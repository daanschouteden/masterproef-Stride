/*
 *  This is free software: you can redistribute it and/or modify it
 *  under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  any later version.
 *  The software is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *  You should have received a copy of the GNU General Public License
 *  along with the software. If not, see <http://www.gnu.org/licenses/>.
 *
 *  Copyright 2020, Willem L, Kuylen E, Broeckhove J
 */

/**
 * @file
 * Implementation of Infector algorithms.
 */

#include "Infector.h"

#include "ContactPool.h"
#include "calendar/Calendar.h"
#include "pop/Person.h"

#include <algorithm>    // std::shuffle
#include <chrono>
#include <iostream>
#include <random>
#include <boost/random.hpp>

#include <unordered_set>

using namespace std::chrono;

using namespace std;

namespace {

/// Primary LOG_POLICY policy, implements LogMode::None.
/// \tparam LL
template <EventLogMode::Id LL>
class LOG_POLICY
{
public:
        static void Contact(const std::shared_ptr<spdlog::logger>&, const Person*, const Person*, ContactType::Id,
                            unsigned short int, const double, const double)
        {
        }

        static void Trans(const std::shared_ptr<spdlog::logger>&, const Person*, const Person*, ContactType::Id,
                          unsigned short int, unsigned int)
        {
        }
};

/// Specialized LOG_POLICY policy LogMode::Transmissions.
template <>
class LOG_POLICY<EventLogMode::Id::Transmissions>
{
public:
        static void Contact(const std::shared_ptr<spdlog::logger>&, const Person*, const Person*, ContactType::Id,
                            unsigned short int, const double, const double)
        {
        }

        static void Trans(const std::shared_ptr<spdlog::logger>& logger, const Person* p1, const Person* p2,
                          ContactType::Id type, unsigned short int sim_day, unsigned int id_index_case)
        {
                logger->info("[TRAN] {} {} {} {} {} {} {} {} {} {} {} {}", p2->GetId(), p1->GetId(), p2->GetAge(), p1->GetAge(),
                             ToString(type), sim_day, id_index_case,
							 p2->GetHealth().GetStartInfectiousness(),p2->GetHealth().GetEndInfectiousness(),
							 p2->GetHealth().GetStartSymptomatic(),p2->GetHealth().GetEndSymptomatic(),
							 p1->GetHealth().IsSymptomatic());
        }
};

/// Specialized LOG_POLICY policy LogMode::All.
template <>
class LOG_POLICY<EventLogMode::Id::All>
{
public:
        static void Contact(const std::shared_ptr<spdlog::logger>& logger, const Person* p1, const Person* p2,
                            ContactType::Id type, unsigned short int sim_day, const double cProb, const double tProb)
        {
                if (p1->IsSurveyParticipant()) {
                        logger->info("[CONT] {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}", p1->GetId(), p1->GetAge(),
                                     p2->GetAge(), static_cast<unsigned int>(type == ContactType::Id::Household),
                                     static_cast<unsigned int>(type == ContactType::Id::K12School),
                                     static_cast<unsigned int>(type == ContactType::Id::College),
                                     static_cast<unsigned int>(type == ContactType::Id::Workplace),
                                     static_cast<unsigned int>(type == ContactType::Id::PrimaryCommunity),
                                     static_cast<unsigned int>(type == ContactType::Id::SecondaryCommunity),
									 static_cast<unsigned int>(type == ContactType::Id::HouseholdCluster),
									 sim_day,
									 cProb, tProb,p2->GetHealth().IsSymptomatic(),p1->GetHealth().IsSymptomatic());
                }
        }

        static void Trans(const std::shared_ptr<spdlog::logger>& logger, const Person* p1, const Person* p2,
                          ContactType::Id type, unsigned short int sim_day, unsigned int id_index_case)
        {
                logger->info("[TRAN] {} {} {} {} {} {} {} {} {} {} {} {}", p2->GetId(), p1->GetId(), p2->GetAge(), p1->GetAge(),
                             ToString(type), sim_day, id_index_case,
							 p2->GetHealth().GetStartInfectiousness(),p2->GetHealth().GetEndInfectiousness(),
							 p2->GetHealth().GetStartSymptomatic(),p2->GetHealth().GetEndSymptomatic(),
							 p1->GetHealth().IsSymptomatic());
        }
};

} // namespace

namespace {

using namespace stride;
using namespace stride::ContactType;

inline double GetContactProbability(const AgeContactProfile& profile, const Person* p1, const Person* p2,
		size_t pool_size, const ContactType::Id pType, double cnt_reduction_work, double cnt_reduction_other,
		double cnt_reduction_school, double cnt_reduction_intergeneration, unsigned int cnt_reduction_intergeneration_cutoff,
		std::shared_ptr<Population>& population, double cnt_intensity_householdCluster)
{

        // initiate a contact adjustment factor, to account for physical distancing and/or contact intensity
    	double cnt_adjustment_factor = 1;

        // account for physical distancing at work and in the community
        if(pType == Id::Workplace){
                cnt_adjustment_factor = (1-cnt_reduction_work);
        }
        // account for physical distancing in the community
        if((pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)){

                // apply inter-generation distancing factor if age cutoff is > 0 and at least one age is > cutoff
                if((cnt_reduction_intergeneration > 0) &&
                        ((p1->GetAge() > cnt_reduction_intergeneration_cutoff) || (p2->GetAge() > cnt_reduction_intergeneration_cutoff))){
                        cnt_adjustment_factor = (1-cnt_reduction_intergeneration);
                } else {
                        // apply uniform community distancing
                        cnt_adjustment_factor = (1-cnt_reduction_other);
                }
        }
        // account for physical distancing at school
        if(pType == Id::K12School){
                cnt_adjustment_factor = (1-cnt_reduction_school);
        }

        // account for contact intensity in household clusters
        if(pType == Id::HouseholdCluster){
                cnt_adjustment_factor = cnt_intensity_householdCluster;
        }


        // get the reference number of contacts, given age and age-contact profile
        double reference_num_contacts_p1{profile[EffectiveAge(static_cast<unsigned int>(p1->GetAge()))]};
        double reference_num_contacts_p2{profile[EffectiveAge(static_cast<unsigned int>(p2->GetAge()))]};
        const double potential_num_contacts{static_cast<double>(pool_size - 1)};

        // adjust contact for distancing
        reference_num_contacts_p1 *= cnt_adjustment_factor;
        reference_num_contacts_p2 *= cnt_adjustment_factor;


        // special case: reduce the number of community contacts if part of a HouseholdCluster
        
        if(cnt_intensity_householdCluster > 0 && (pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)){

        	// get the number of non-household members in the HouseholdCluster
        	double householdCluster_non_household_members_p1 = static_cast<double>(population->GetPoolSize(Id::HouseholdCluster,p1)) -
        											                  population->GetPoolSize(Id::Household,p1);

        	double householdCluster_non_household_members_p2 = static_cast<double>(population->GetPoolSize(Id::HouseholdCluster,p2)) -
        	        											      population->GetPoolSize(Id::Household,p2);

        	// account for negative values ==>> not part of a HouseholdCluster
        	householdCluster_non_household_members_p1 = householdCluster_non_household_members_p1 < 0 ? 0 : householdCluster_non_household_members_p1;
        	householdCluster_non_household_members_p2 = householdCluster_non_household_members_p2 < 0 ? 0 : householdCluster_non_household_members_p2;

        	// account for the HouseholdCluster size and contact intensity
        	reference_num_contacts_p1 -= householdCluster_non_household_members_p1 * cnt_intensity_householdCluster;
        	reference_num_contacts_p2 -= householdCluster_non_household_members_p2 * cnt_intensity_householdCluster;

        	// account for negative values
        	reference_num_contacts_p1 = reference_num_contacts_p1 < 0 ? 0 : reference_num_contacts_p1;
        	reference_num_contacts_p2 = reference_num_contacts_p2 < 0 ? 0 : reference_num_contacts_p2;
        } 
        
        // calculate the contact probability based on the (possible) number of contacts
        double individual_contact_probability_p1 = reference_num_contacts_p1 / potential_num_contacts;
        double individual_contact_probability_p2 = reference_num_contacts_p2 / potential_num_contacts;

        // use the minimum of both age-specific probabilities
        double contact_probability = individual_contact_probability_p1 ;
        if(individual_contact_probability_p2 < individual_contact_probability_p1){
                contact_probability = individual_contact_probability_p2;
        }

        // limit probability to 0.999
        if (contact_probability >= 1) {
        	contact_probability = 0.999;
        }

    	// assume fully connected households
        if(pType == Id::Household){
                contact_probability = 0.999;
        }

        // exclude contacts with household members within household cluster
        if(pType == Id::HouseholdCluster){
                contact_probability = (p1->GetPoolId(Id::Household) == p2->GetPoolId(Id::Household)) ? 0.0 : cnt_intensity_householdCluster;
        }


        return contact_probability;
}


// Used for sampling approaches
inline double CustomGetContactProbability(double reference_num_contacts, const size_t pool_size, const ContactType::Id pType,
                                 const unsigned int age1, const unsigned int age2,
                                double cnt_reduction_work, double cnt_reduction_intergeneration, double cnt_reduction_other,
                                unsigned int cnt_reduction_intergeneration_cutoff)
{
        // initiate a contact adjustment factor, to account for physical distancing and/or contact intensity
        double cnt_adjustment_factor = 1;
        // account for physical distancing at work and in the community
        if(pType == Id::Workplace){
                cnt_adjustment_factor = (1-cnt_reduction_work);
        }
        // account for physical distancing in the community
        else if((pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)){
                // apply inter-generation distancing factor if age cutoff is > 0 and at least one age is > cutoff
                if((cnt_reduction_intergeneration > 0) && 
                ((age1 > cnt_reduction_intergeneration_cutoff) || (age2 > cnt_reduction_intergeneration_cutoff))){
                        cnt_adjustment_factor = (1-cnt_reduction_intergeneration);

                } else {
                        // apply uniform community distancing
                        cnt_adjustment_factor = (1-cnt_reduction_other);
                }
        }
        
        reference_num_contacts *= cnt_adjustment_factor;
        double contactProb = reference_num_contacts / (pool_size-1);

        if (contactProb >= 1) {
                contactProb = 0.999;
        }

        return contactProb;
}

} // namespace

namespace stride {

//-------------------------------------------------------------------------------------------------
// Definition for ContactLogMode::Contacts,
// both with track_index_case false and true.
//-------------------------------------------------------------------------------------------------
template <EventLogMode::Id LL, bool TIC, bool TO>
void Infector<LL, TIC, TO>::Exec(ContactPool& pool, const AgeContactProfile& profile,
                                 const TransmissionProfile& transProfile, ContactHandler& cHandler,
                                 unsigned short int simDay, shared_ptr<spdlog::logger> eventLogger,
								 double cnt_reduction_work, double cnt_reduction_other, double cnt_reduction_school,
								 double cnt_reduction_intergeneration, unsigned int cnt_reduction_intergeneration_cutoff,
								 std::shared_ptr<Population> population, double m_cnt_intensity_householdCluster,
                                                                 std::vector<long>& times, std::vector<int>& counts)
{
        using LP = LOG_POLICY<LL>;

        // set up some stuff
        const auto  pType    = pool.m_pool_type;
        const auto& pMembers = pool.m_members;
        const auto  pSize    = pMembers.size();         // const auto  pSize    = pool.PeopleInPool();
        const auto  tProb    = transProfile.GetProbability();

        if (pSize >= 1500) {
                cout << "ffs: " << pSize << endl;
                return;
        }

        auto start = high_resolution_clock::now();

        // Intervals without sampling
        if (false && pSize <= 125 && pType == Id::Workplace) {
        // if (false && pType == Id::SecondaryCommunity) {

                const auto pIntervalAmounts = pool.SortMembersByAgeIntervalsYO();
                const auto pNumberOfIntervals = pIntervalAmounts.size();

                unsigned int index = 0;
                for (unsigned int interval1 = 0; interval1 < pNumberOfIntervals; interval1++) {
                        unsigned int people_in_interval1 = pIntervalAmounts[interval1];
                        if (people_in_interval1 == 0) {
                                continue;
                        }

                        double reference_num_contacts1 = profile[EffectiveAge(static_cast<unsigned int>(pMembers[index]->GetAge()))];

                        unsigned int index2 = index;
                        for (unsigned int interval2 = interval1; interval2 < pNumberOfIntervals; interval2++) {
                                unsigned int people_in_interval2 = pIntervalAmounts[interval2];
                                if (people_in_interval2 == 0) {
                                        continue;
                                }

                                // Compare everyone from the same interval too
                                if (interval1 == interval2) {
                                        double reference_num_contacts = reference_num_contacts1;

                                        // initiate a contact adjustment factor, to account for physical distancing and/or contact intensity
                                        double cnt_adjustment_factor = 1;
                                        // account for physical distancing at work and in the community
                                        if(pType == Id::Workplace){
                                                cnt_adjustment_factor = (1-cnt_reduction_work);
                                        }
                                        // account for physical distancing in the community
                                        else if((pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)){
                                                // apply inter-generation distancing factor if age cutoff is > 0 and at least one age is > cutoff
                                                if((cnt_reduction_intergeneration > 0) &&
                                                ((pMembers[index]->GetAge() > cnt_reduction_intergeneration_cutoff) || (pMembers[index2]->GetAge() > cnt_reduction_intergeneration_cutoff))){
                                                        cnt_adjustment_factor = (1-cnt_reduction_intergeneration);
                                                } else {
                                                        // apply uniform community distancing
                                                        cnt_adjustment_factor = (1-cnt_reduction_other);
                                                }
                                        }
                                        
                                        reference_num_contacts *= cnt_adjustment_factor;
                                        double contactProb = reference_num_contacts / (pSize-1);
                                        if (contactProb >= 1) {
                                                contactProb = 0.999;
                                        }

                                        for (size_t i_person1 = 0; i_person1 < pIntervalAmounts[interval1]; i_person1++) {
                                                const auto p1 = pMembers[i_person1+index];
                                                if (!p1->IsInPool(pType)) {
                                                        continue;
                                                }
                                                for (size_t i_contact = i_person1+1; i_contact < pIntervalAmounts[interval2]; i_contact++) {
                                                        // Check if member is present today
                                                        const auto p2 = pMembers[i_contact+index2];   
                                                        if (!p2->IsInPool(pType)) {
                                                                continue;
                                                        }

                                                        if (cHandler.HasContact(contactProb)) {
                                                                // log contact if person 1 is participating in survey
                                                                LP::Contact(eventLogger, p1, p2, pType, simDay, contactProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                                                // log contact if person 2 is participating in survey
                                                                LP::Contact(eventLogger, p2, p1, pType, simDay, contactProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2);
                                                                p2->RegisterContact(p1);

                                                                // transmission & infection.
                                                                // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                                                auto& h1 = p1->GetHealth();
                                                                auto& h2 = p2->GetHealth();

                                                                // if h1 infectious, account for susceptibility of p2
                                                                if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                                        cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                                h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                                                if (TIC)
                                                                                                h2.StopInfection();
                                                                                LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                                }

                                                                // if h2 infectious, account for susceptibility of p1
                                                                if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                                        cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                                                h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                                                if (TIC)
                                                                                                h1.StopInfection();
                                                                                LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                                                }
                                                        }
                                                }
                                        }
                                }
                                else {
                                        double reference_num_contacts2 = profile[EffectiveAge(static_cast<unsigned int>(pMembers[index2]->GetAge()))];

                                        double reference_num_contacts = min(reference_num_contacts1, reference_num_contacts2);

                                        // initiate a contact adjustment factor, to account for physical distancing and/or contact intensity
                                        double cnt_adjustment_factor = 1;
                                        // account for physical distancing at work and in the community
                                        if(pType == Id::Workplace){
                                                cnt_adjustment_factor = (1-cnt_reduction_work);
                                        }
                                        // account for physical distancing in the community
                                        else if((pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)){
                                                // apply inter-generation distancing factor if age cutoff is > 0 and at least one age is > cutoff
                                                if((cnt_reduction_intergeneration > 0) && 
                                                ((pMembers[index]->GetAge() > cnt_reduction_intergeneration_cutoff) || (pMembers[index2]->GetAge() > cnt_reduction_intergeneration_cutoff))){
                                                        cnt_adjustment_factor = (1-cnt_reduction_intergeneration);

                                                } else {
                                                        // apply uniform community distancing
                                                        cnt_adjustment_factor = (1-cnt_reduction_other);
                                                }
                                        }
                                        
                                        reference_num_contacts *= cnt_adjustment_factor;
                                        double contactProb = reference_num_contacts / (pSize-1);
                                        if (contactProb >= 1) {
                                                contactProb = 0.999;
                                        }

                                        for (size_t i_interval1 = 0; i_interval1 < pIntervalAmounts[interval1]; i_interval1++) {
                                                // Check if member is present today
                                                const auto p1 = pMembers[i_interval1+index];
                                                if (!p1->IsInPool(pType)) {
                                                        continue;
                                                }

                                                for (size_t i_interval2 = 0; i_interval2 < pIntervalAmounts[interval2]; i_interval2++) {
                                                        // Check if member is present today
                                                        const auto p2 = pMembers[i_interval2+index2];
                                                        if (!p2->IsInPool(pType)) {
                                                                continue;
                                                        }

                                                        if (cHandler.HasContact(contactProb)) {
                                                                // log contact if person 1 is participating in survey
                                                                LP::Contact(eventLogger, p1, p2, pType, simDay, contactProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                                                // log contact if person 2 is participating in survey
                                                                LP::Contact(eventLogger, p2, p1, pType, simDay, contactProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2);
                                                                p2->RegisterContact(p1);

                                                                // transmission & infection.
                                                                // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                                                auto& h1 = p1->GetHealth();
                                                                auto& h2 = p2->GetHealth();

                                                                // if h1 infectious, account for susceptibility of p2
                                                                if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                                        if (TIC)
                                                                                h2.StopInfection();
                                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                                }

                                                                // if h2 infectious, account for susceptibility of p1
                                                                if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                                        h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                                        if (TIC)
                                                                                h1.StopInfection();
                                                                        LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                                                }
                                                        }
                                                }
                                        }
                                }
                                index2 += pIntervalAmounts[interval2];
                        }
                        index += pIntervalAmounts[interval1];
                }
        }
        
        // Sampling also in same interval
        //else if (pSize >= 100) {
        else if (false && pType == Id::Workplace) {

                const auto pIntervalAmounts = pool.SortMembersByAgeIntervalsYO();
                const auto pNumberOfIntervals = pIntervalAmounts.size();

                std::random_device rd;
                std::mt19937 gen(rd());

                unsigned int index = 0;
                for (unsigned int interval1 = 0; interval1 < pNumberOfIntervals; interval1++) {
                        unsigned int people_in_interval1 = pIntervalAmounts[interval1];
                        if (people_in_interval1 == 0) {
                                continue;
                        }

                        double reference_num_contacts1 = profile[EffectiveAge(static_cast<unsigned int>(pMembers[index]->GetAge()))];

                        unsigned int index2 = index;
                        for (unsigned int interval2 = interval1; interval2 < pNumberOfIntervals; interval2++) {
                                unsigned int people_in_interval2 = pIntervalAmounts[interval2];
                                if (people_in_interval2 == 0) {
                                        continue;
                                }

                                // Compare everyone from the same interval too
                                if (interval1 == interval2) {
                                        double reference_num_contacts = reference_num_contacts1;

                                        // initiate a contact adjustment factor, to account for physical distancing and/or contact intensity
                                        double cnt_adjustment_factor = 1;
                                        // account for physical distancing at work and in the community
                                        if(pType == Id::Workplace){
                                                cnt_adjustment_factor = (1-cnt_reduction_work);
                                        }
                                        // account forinterval2 physical distancing in the community
                                        else if((pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)){
                                                // apply inter-generation distancing factor if age cutoff is > 0 and at least one age is > cutoff
                                                if((cnt_reduction_intergeneration > 0) &&
                                                ((pMembers[index]->GetAge() > cnt_reduction_intergeneration_cutoff) || (pMembers[index2]->GetAge() > cnt_reduction_intergeneration_cutoff))){
                                                        cnt_adjustment_factor = (1-cnt_reduction_intergeneration);
                                                } else {
                                                        // apply uniform community distancing
                                                        cnt_adjustment_factor = (1-cnt_reduction_other);
                                                }
                                        }
                                        
                                        reference_num_contacts *= cnt_adjustment_factor;

                                        double contactProb = (2 - sqrt(4-(4*(reference_num_contacts1/(pSize-1))))) / 2;

                                        if (contactProb >= 1) {
                                                contactProb = 0.999;
                                        }

                                        binomial_distribution<int> distr(people_in_interval1, contactProb);

                                        for (size_t i_person1 = 0; i_person1 < pIntervalAmounts[interval1]; i_person1++) {
                                                const auto p1 = pMembers[i_person1+index];
                                                if (!p1->IsInPool(pType)) {
                                                        continue;
                                                }
                                                // The number of people 1 person will have contact with
                                                int sampleSize = distr(gen);
                                                if (sampleSize == 0) {
                                                        continue;
                                                }

                                                // Every remaining person will have contact
                                                if (sampleSize >= people_in_interval2) {
                                                        for (size_t i_contact = 0; i_contact < pIntervalAmounts[interval2]; i_contact++) {
                                                                // Check if member is present today
                                                                const auto p2 = pMembers[i_contact+index2];
                                                                if (!p2->IsInPool(pType) || p1 == p2) {
                                                                        continue;
                                                                }

                                                                // log contact if person 1 is participating in survey
                                                                LP::Contact(eventLogger, p1, p2, pType, simDay, contactProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                                                // log contact if person 2 is participating in survey
                                                                LP::Contact(eventLogger, p2, p1, pType, simDay, contactProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2);
                                                                p2->RegisterContact(p1);

                                                                // transmission & infection.
                                                                // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                                                auto& h1 = p1->GetHealth();
                                                                auto& h2 = p2->GetHealth();

                                                                // if h1 infectious, account for susceptibility of p2
                                                                if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                                        if (TIC)
                                                                                h2.StopInfection();
                                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                                }

                                                                // if h2 infectious, account for susceptibility of p1
                                                                if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                                        h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                                        if (TIC)
                                                                                h1.StopInfection();
                                                                        LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                                                }
                                                        }
                                                }
                                                else {
                                                        unsigned int sampled = 1; // Because p1 is already drawn
                                                        unsigned int good_samples = 0;

                                                        std::vector<int> drawn_samples(people_in_interval2, -1);
                                                        // The person can not draw itself
                                                        drawn_samples[0] = i_person1+index;

                                                        /*stop if:
                                                        1) drawn the required samples
                                                        2) when everyone of the interval has been picked
                                                        Number 2 is made to prevent infinite looping when less people are present in the pool than sampleSize
                                                        */
                                                        while ((good_samples < sampleSize) && (sampled < people_in_interval2)) {

                                                                int i_sampled = (int) (cHandler()*people_in_interval2) + index2;

                                                                // i_sampled has already been drawn
                                                                if ( std::find(drawn_samples.begin(), drawn_samples.begin()+sampled, i_sampled) != drawn_samples.begin()+sampled ) {
                                                                        continue;
                                                                }
                                                                
                                                                drawn_samples[sampled] = i_sampled;
                                                                sampled++;

                                                                // Check if member is present today
                                                                const auto p2 = pMembers[i_sampled];
                                                                if (!p2->IsInPool(pType)) {
                                                                        continue;
                                                                }
                                                                good_samples++;

                                                                // log contact if person 1 is participating in survey
                                                                LP::Contact(eventLogger, p1, p2, pType, simDay, contactProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                                                // log contact if person 2 is participating in survey
                                                                LP::Contact(eventLogger, p2, p1, pType, simDay, contactProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2);
                                                                p2->RegisterContact(p1);

                                                                // transmission & infection.
                                                                // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                                                auto& h1 = p1->GetHealth();
                                                                auto& h2 = p2->GetHealth();

                                                                // if h1 infectious, account for susceptibility of p2
                                                                if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                                        if (TIC)
                                                                                h2.StopInfection();
                                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                                }

                                                                // if h2 infectious, account for susceptibility of p1
                                                                if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                                        h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                                        if (TIC)
                                                                                h1.StopInfection();
                                                                        LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                                                }
                                                        }
                                                }
                                        }
                                        /*
                                        for (size_t i_person1 = 0; i_person1 < pIntervalAmounts[interval1]; i_person1++) {
                                                const auto p1 = pMembers[i_person1+index];
                                                if (!p1->IsInPool(pType)) {
                                                        continue;
                                                }
                                                for (size_t i_contact = i_person1+1; i_contact < pIntervalAmounts[interval2]; i_contact++) {
                                                        // Check if member is present today
                                                        const auto p2 = pMembers[i_contact+index2];   
                                                        if (!p2->IsInPool(pType)) {
                                                                continue;
                                                        }

                                                        if (cHandler.HasContact(contactProb)) {
                                                                // log contact if person 1 is participating in survey
                                                                LP::Contact(eventLogger, p1, p2, pType, simDay, contactProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                                                // log contact if person 2 is participating in survey
                                                                LP::Contact(eventLogger, p2, p1, pType, simDay, contactProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2);
                                                                p2->RegisterContact(p1);

                                                                // transmission & infection.
                                                                // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                                                auto& h1 = p1->GetHealth();
                                                                auto& h2 = p2->GetHealth();

                                                                // if h1 infectious, account for susceptibility of p2
                                                                if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                                        cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                                h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                                                if (TIC)
                                                                                                h2.StopInfection();
                                                                                LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                                }

                                                                // if h2 infectious, account for susceptibility of p1
                                                                if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                                        cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                                                h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                                                if (TIC)
                                                                                                h1.StopInfection();
                                                                                LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                                                }
                                                        }
                                                }
                                        }
                                        */
                                }
                                else {
                                        double reference_num_contacts2 = profile[EffectiveAge(static_cast<unsigned int>(pMembers[index2]->GetAge()))];

                                        double reference_num_contacts = min(reference_num_contacts1, reference_num_contacts2);

                                        // initiate a contact adjustment factor, to account for physical distancing and/or contact intensity
                                        double cnt_adjustment_factor = 1;
                                        // account for physical distancing at work and in the community
                                        if(pType == Id::Workplace){
                                                cnt_adjustment_factor = (1-cnt_reduction_work);
                                        }
                                        // account for physical distancing in the community
                                        else if((pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)){
                                                // apply inter-generation distancing factor if age cutoff is > 0 and at least one age is > cutoff
                                                if((cnt_reduction_intergeneration > 0) && 
                                                ((pMembers[index]->GetAge() > cnt_reduction_intergeneration_cutoff) || (pMembers[index2]->GetAge() > cnt_reduction_intergeneration_cutoff))){
                                                        cnt_adjustment_factor = (1-cnt_reduction_intergeneration);

                                                } else {
                                                        // apply uniform community distancing
                                                        cnt_adjustment_factor = (1-cnt_reduction_other);
                                                }
                                        }
                                        
                                        reference_num_contacts *= cnt_adjustment_factor;
                                        double contactProb = reference_num_contacts / (pSize-1);
                                        if (contactProb >= 1) {
                                                contactProb = 0.999;
                                        }

                                        binomial_distribution<int> distr(people_in_interval2, contactProb);

                                        for (size_t i_person1 = 0; i_person1 < pIntervalAmounts[interval1]; i_person1++) {
                                                const auto p1 = pMembers[i_person1+index];
                                                if (!p1->IsInPool(pType)) {
                                                        continue;
                                                }
                                                // The number of people 1 person will have contact with
                                                int sampleSize = distr(gen);
                                                if (sampleSize == 0) {
                                                        continue;
                                                }


                                                // Every remaining person will have contact
                                                if (sampleSize >= people_in_interval2) {
                                                        for (size_t i_contact = 0; i_contact < pIntervalAmounts[interval2]; i_contact++) {
                                                                // Check if member is present today
                                                                const auto p2 = pMembers[i_contact+index2];
                                                                if (!p2->IsInPool(pType)) {
                                                                        continue;
                                                                }

                                                                // log contact if person 1 is participating in survey
                                                                LP::Contact(eventLogger, p1, p2, pType, simDay, contactProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                                                // log contact if person 2 is participating in survey
                                                                LP::Contact(eventLogger, p2, p1, pType, simDay, contactProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2);
                                                                p2->RegisterContact(p1);

                                                                // transmission & infection.
                                                                // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                                                auto& h1 = p1->GetHealth();
                                                                auto& h2 = p2->GetHealth();

                                                                // if h1 infectious, account for susceptibility of p2
                                                                if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                                        if (TIC)
                                                                                h2.StopInfection();
                                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                                }

                                                                // if h2 infectious, account for susceptibility of p1
                                                                if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                                        h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                                        if (TIC)
                                                                                h1.StopInfection();
                                                                        LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                                                }
                                                        }
                                                }
                                                else {
                                                        unsigned int sampled = 0;
                                                        unsigned int good_samples = 0;

                                                        std::vector<int> drawn_samples(people_in_interval2, -1);

                                                        /*stop if:
                                                        1) drawn the required samples
                                                        2) when everyone of the interval has been picked
                                                        Number 2 is made to prevent infinite looping when less people are present in the pool than sampleSize
                                                        */
                                                        while ((good_samples < sampleSize) && (sampled < people_in_interval2)) {

                                                                int i_sampled = (int) (cHandler()*people_in_interval2) + index2;

                                                                // i_sampled has already been drawn
                                                                if ( std::find(drawn_samples.begin(), drawn_samples.begin()+sampled, i_sampled) != drawn_samples.begin()+sampled ) {
                                                                        continue;
                                                                }
                                                                
                                                                drawn_samples[sampled] = i_sampled;
                                                                sampled++;

                                                                // Check if member is present today
                                                                const auto p2 = pMembers[i_sampled];
                                                                if (!p2->IsInPool(pType)) {
                                                                        continue;
                                                                }
                                                                good_samples++;

                                                                // log contact if person 1 is participating in survey
                                                                LP::Contact(eventLogger, p1, p2, pType, simDay, contactProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                                                // log contact if person 2 is participating in survey
                                                                LP::Contact(eventLogger, p2, p1, pType, simDay, contactProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2);
                                                                p2->RegisterContact(p1);

                                                                // transmission & infection.
                                                                // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                                                auto& h1 = p1->GetHealth();
                                                                auto& h2 = p2->GetHealth();

                                                                // if h1 infectious, account for susceptibility of p2
                                                                if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                                        if (TIC)
                                                                                h2.StopInfection();
                                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                                }

                                                                // if h2 infectious, account for susceptibility of p1
                                                                if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                                        h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                                        if (TIC)
                                                                                h1.StopInfection();
                                                                        LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                                                }
                                                        }
                                                }
                                        }
                                }
                                index2 += pIntervalAmounts[interval2];
                        }
                        index += pIntervalAmounts[interval1];
                }
        }
        
        // Sampling
        //else if(pSize >= 100) {
        else if(pSize >= 100){ //&& (pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)) {

                const auto pIntervalAmounts = pool.SortMembersByAgeIntervalsYO();
                const auto pNumberOfIntervals = pIntervalAmounts.size();

                std::random_device rd;
                std::mt19937 gen(rd());

                unsigned int index = 0;
                for (unsigned int interval1 = 0; interval1 < pNumberOfIntervals; interval1++) {
                        unsigned int people_in_interval1 = pIntervalAmounts[interval1];
                        if (people_in_interval1 == 0) {
                                continue;
                        }

                        double reference_num_contacts1 = profile[EffectiveAge(static_cast<unsigned int>(pMembers[index]->GetAge()))];

                        unsigned int index2 = index;
                        for (unsigned int interval2 = interval1; interval2 < pNumberOfIntervals; interval2++) {
                                unsigned int people_in_interval2 = pIntervalAmounts[interval2];
                                if (people_in_interval2 == 0) {
                                        continue;
                                }

                                // Compare everyone from the same interval too
                                if (interval1 == interval2) {
                                        double reference_num_contacts = reference_num_contacts1;

                                        // initiate a contact adjustment factor, to account for physical distancing and/or contact intensity
                                        double cnt_adjustment_factor = 1;
                                        // account for physical distancing at work and in the community
                                        if(pType == Id::Workplace){
                                                cnt_adjustment_factor = (1-cnt_reduction_work);
                                        }
                                        // account forinterval2 physical distancing in the community
                                        else if((pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)){
                                                // apply inter-generation distancing factor if age cutoff is > 0 and at least one age is > cutoff
                                                if((cnt_reduction_intergeneration > 0) &&
                                                ((pMembers[index]->GetAge() > cnt_reduction_intergeneration_cutoff) || (pMembers[index2]->GetAge() > cnt_reduction_intergeneration_cutoff))){
                                                        cnt_adjustment_factor = (1-cnt_reduction_intergeneration);
                                                } else {
                                                        // apply uniform community distancing
                                                        cnt_adjustment_factor = (1-cnt_reduction_other);
                                                }
                                        }
                                        
                                        reference_num_contacts *= cnt_adjustment_factor;
                                        double contactProb = reference_num_contacts / (pSize-1);
                                        if (contactProb >= 1) {
                                                contactProb = 0.999;
                                        }

                                        for (size_t i_person1 = 0; i_person1 < pIntervalAmounts[interval1]; i_person1++) {
                                                const auto p1 = pMembers[i_person1+index];
                                                if (!p1->IsInPool(pType)) {
                                                        continue;
                                                }
                                                for (size_t i_contact = i_person1+1; i_contact < pIntervalAmounts[interval2]; i_contact++) {
                                                        // Check if member is present today
                                                        const auto p2 = pMembers[i_contact+index2];   
                                                        if (!p2->IsInPool(pType)) {
                                                                continue;
                                                        }

                                                        if (cHandler.HasContact(contactProb)) {
                                                                // log contact if person 1 is participating in survey
                                                                LP::Contact(eventLogger, p1, p2, pType, simDay, contactProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                                                // log contact if person 2 is participating in survey
                                                                LP::Contact(eventLogger, p2, p1, pType, simDay, contactProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2);
                                                                p2->RegisterContact(p1);

                                                                // transmission & infection.
                                                                // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                                                auto& h1 = p1->GetHealth();
                                                                auto& h2 = p2->GetHealth();

                                                                // if h1 infectious, account for susceptibility of p2
                                                                if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                                        cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                                h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                                                if (TIC)
                                                                                                h2.StopInfection();
                                                                                LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                                }

                                                                // if h2 infectious, account for susceptibility of p1
                                                                if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                                        cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                                                h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                                                if (TIC)
                                                                                                h1.StopInfection();
                                                                                LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                                                }
                                                        }
                                                }
                                        }
                                }
                                else {
                                        double reference_num_contacts2 = profile[EffectiveAge(static_cast<unsigned int>(pMembers[index2]->GetAge()))];

                                        double reference_num_contacts = min(reference_num_contacts1, reference_num_contacts2);

                                        double contactProb = CustomGetContactProbability(reference_num_contacts, pSize, pType,
                                                                EffectiveAge(static_cast<unsigned int>(pMembers[index]->GetAge())),
                                                                EffectiveAge(static_cast<unsigned int>(pMembers[index2]->GetAge())),
                                                                cnt_reduction_work, cnt_reduction_intergeneration, cnt_reduction_other,
                                                                cnt_reduction_intergeneration_cutoff);

                                        binomial_distribution<int> distr(people_in_interval2, contactProb);

                                        for (size_t i_person1 = 0; i_person1 < pIntervalAmounts[interval1]; i_person1++) {
                                                const auto p1 = pMembers[i_person1+index];
                                                if (!p1->IsInPool(pType)) {
                                                        continue;
                                                }
                                                // The number of people 1 person will have contact with
                                                int sampleSize = distr(gen);
                                                if (sampleSize == 0) {
                                                        continue;
                                                }


                                                // Every remaining person will have contact
                                                if (sampleSize >= people_in_interval2) {
                                                        for (size_t i_contact = 0; i_contact < pIntervalAmounts[interval2]; i_contact++) {
                                                                // Check if member is present today
                                                                const auto p2 = pMembers[i_contact+index2];
                                                                if (!p2->IsInPool(pType)) {
                                                                        continue;
                                                                }

                                                                // log contact if person 1 is participating in survey
                                                                LP::Contact(eventLogger, p1, p2, pType, simDay, contactProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                                                // log contact if person 2 is participating in survey
                                                                LP::Contact(eventLogger, p2, p1, pType, simDay, contactProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2);
                                                                p2->RegisterContact(p1);

                                                                // transmission & infection.
                                                                // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                                                auto& h1 = p1->GetHealth();
                                                                auto& h2 = p2->GetHealth();

                                                                // if h1 infectious, account for susceptibility of p2
                                                                if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                                        if (TIC)
                                                                                h2.StopInfection();
                                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                                }

                                                                // if h2 infectious, account for susceptibility of p1
                                                                if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                                        h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                                        if (TIC)
                                                                                h1.StopInfection();
                                                                        LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                                                }
                                                        }
                                                }
                                                else {
                                                        unsigned int sampled = 0;
                                                        unsigned int good_samples = 0;

                                                        std::vector<int> drawn_samples(people_in_interval2, -1);

                                                        /*stop if:
                                                        1) drawn the required samples
                                                        2) when everyone of the interval has been picked
                                                        Number 2 is made to prevent infinite looping when less people are present in the pool than sampleSize
                                                        */
                                                        while ((good_samples < sampleSize) && (sampled < people_in_interval2)) {

                                                                int i_sampled = (int) (cHandler()*people_in_interval2) + index2;

                                                                // i_sampled has already been drawn
                                                                if ( std::find(drawn_samples.begin(), drawn_samples.begin()+sampled, i_sampled) != drawn_samples.begin()+sampled ) {
                                                                        continue;
                                                                }
                                                                
                                                                drawn_samples[sampled] = i_sampled;
                                                                sampled++;

                                                                // Check if member is present today
                                                                const auto p2 = pMembers[i_sampled];
                                                                if (!p2->IsInPool(pType)) {
                                                                        continue;
                                                                }
                                                                good_samples++;

                                                                // log contact if person 1 is participating in survey
                                                                LP::Contact(eventLogger, p1, p2, pType, simDay, contactProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                                                // log contact if person 2 is participating in survey
                                                                LP::Contact(eventLogger, p2, p1, pType, simDay, contactProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2);
                                                                p2->RegisterContact(p1);

                                                                // transmission & infection.
                                                                // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                                                auto& h1 = p1->GetHealth();
                                                                auto& h2 = p2->GetHealth();

                                                                // if h1 infectious, account for susceptibility of p2
                                                                if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                                        if (TIC)
                                                                                h2.StopInfection();
                                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                                }

                                                                // if h2 infectious, account for susceptibility of p1
                                                                if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                                        h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                                        if (TIC)
                                                                                h1.StopInfection();
                                                                        LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                                                }
                                                        }
                                                }
                                        }
                                }
                                index2 += pIntervalAmounts[interval2];
                        }
                        index += pIntervalAmounts[interval1];
                }
        }
        
        // Sampling with unordered_set
        else if (false) {
        //else if (pSize >= 100) {
        // else if(false && pType == Id::Workplace) {
                const auto pIntervalAmounts = pool.SortMembersByAgeIntervalsYO();
                const auto pNumberOfIntervals = pIntervalAmounts.size();

                std::random_device rd;
                std::mt19937 gen(rd());

                unsigned int index = 0;
                for (unsigned int interval1 = 0; interval1 < pNumberOfIntervals; interval1++) {
                        unsigned int people_in_interval1 = pIntervalAmounts[interval1];
                        if (people_in_interval1 == 0) {
                                continue;
                        }

                        double reference_num_contacts1 = profile[EffectiveAge(static_cast<unsigned int>(pMembers[index]->GetAge()))];

                        unsigned int index2 = index;
                        for (unsigned int interval2 = interval1; interval2 < pNumberOfIntervals; interval2++) {
                                unsigned int people_in_interval2 = pIntervalAmounts[interval2];
                                if (people_in_interval2 == 0) {
                                        continue;
                                }

                                // Compare everyone from the same interval too
                                if (interval1 == interval2) {
                                        double reference_num_contacts = reference_num_contacts1;

                                        // initiate a contact adjustment factor, to account for physical distancing and/or contact intensity
                                        double cnt_adjustment_factor = 1;
                                        // account for physical distancing at work and in the community
                                        if(pType == Id::Workplace){
                                                cnt_adjustment_factor = (1-cnt_reduction_work);
                                        }
                                        // account forinterval2 physical distancing in the community
                                        else if((pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)){
                                                // apply inter-generation distancing factor if age cutoff is > 0 and at least one age is > cutoff
                                                if((cnt_reduction_intergeneration > 0) &&
                                                ((pMembers[index]->GetAge() > cnt_reduction_intergeneration_cutoff) || (pMembers[index2]->GetAge() > cnt_reduction_intergeneration_cutoff))){
                                                        cnt_adjustment_factor = (1-cnt_reduction_intergeneration);
                                                } else {
                                                        // apply uniform community distancing
                                                        cnt_adjustment_factor = (1-cnt_reduction_other);
                                                }
                                        }
                                        
                                        reference_num_contacts *= cnt_adjustment_factor;
                                        double contactProb = reference_num_contacts / (pSize-1);
                                        if (contactProb >= 1) {
                                                contactProb = 0.999;
                                        }

                                        for (size_t i_person1 = 0; i_person1 < pIntervalAmounts[interval1]; i_person1++) {
                                                const auto p1 = pMembers[i_person1+index];
                                                if (!p1->IsInPool(pType)) {
                                                        continue;
                                                }
                                                for (size_t i_contact = i_person1+1; i_contact < pIntervalAmounts[interval2]; i_contact++) {
                                                        // Check if member is present today
                                                        const auto p2 = pMembers[i_contact+index2];   
                                                        if (!p2->IsInPool(pType)) {
                                                                continue;
                                                        }

                                                        if (cHandler.HasContact(contactProb)) {
                                                                // log contact if person 1 is participating in survey
                                                                LP::Contact(eventLogger, p1, p2, pType, simDay, contactProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                                                // log contact if person 2 is participating in survey
                                                                LP::Contact(eventLogger, p2, p1, pType, simDay, contactProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2);
                                                                p2->RegisterContact(p1);

                                                                // transmission & infection.
                                                                // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                                                auto& h1 = p1->GetHealth();
                                                                auto& h2 = p2->GetHealth();

                                                                // if h1 infectious, account for susceptibility of p2
                                                                if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                                        cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                                h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                                                if (TIC)
                                                                                                h2.StopInfection();
                                                                                LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                                }

                                                                // if h2 infectious, account for susceptibility of p1
                                                                if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                                        cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                                                h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                                                if (TIC)
                                                                                                h1.StopInfection();
                                                                                LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                                                }
                                                        }
                                                }
                                        }
                                }
                                else {
                                        double reference_num_contacts2 = profile[EffectiveAge(static_cast<unsigned int>(pMembers[index2]->GetAge()))];

                                        double reference_num_contacts = min(reference_num_contacts1, reference_num_contacts2);

                                        // initiate a contact adjustment factor, to account for physical distancing and/or contact intensity
                                        double cnt_adjustment_factor = 1;
                                        // account for physical distancing at work and in the community
                                        if(pType == Id::Workplace){
                                                cnt_adjustment_factor = (1-cnt_reduction_work);
                                        }
                                        // account for physical distancing in the community
                                        else if((pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)){
                                                // apply inter-generation distancing factor if age cutoff is > 0 and at least one age is > cutoff
                                                if((cnt_reduction_intergeneration > 0) && 
                                                ((pMembers[index]->GetAge() > cnt_reduction_intergeneration_cutoff) || (pMembers[index2]->GetAge() > cnt_reduction_intergeneration_cutoff))){
                                                        cnt_adjustment_factor = (1-cnt_reduction_intergeneration);

                                                } else {
                                                        // apply uniform community distancing
                                                        cnt_adjustment_factor = (1-cnt_reduction_other);
                                                }
                                        }
                                        
                                        reference_num_contacts *= cnt_adjustment_factor;
                                        double contactProb = reference_num_contacts / (pSize-1);
                                        if (contactProb >= 1) {
                                                contactProb = 0.999;
                                        }

                                        binomial_distribution<int> distr(people_in_interval2, contactProb);

                                        for (size_t i_person1 = 0; i_person1 < pIntervalAmounts[interval1]; i_person1++) {
                                                const auto p1 = pMembers[i_person1+index];
                                                if (!p1->IsInPool(pType)) {
                                                        continue;
                                                }
                                                // The number of people 1 person will have contact with
                                                int sampleSize = distr(gen);
                                                if (sampleSize == 0) {
                                                        continue;
                                                }

                                                // Every remaining person will have contact
                                                if (sampleSize >= people_in_interval2) {
                                                        for (size_t i_contact = 0; i_contact < pIntervalAmounts[interval2]; i_contact++) {
                                                                // Check if member is present today
                                                                const auto p2 = pMembers[i_contact+index2];
                                                                if (!p2->IsInPool(pType)) {
                                                                        continue;
                                                                }

                                                                // log contact if person 1 is participating in survey
                                                                LP::Contact(eventLogger, p1, p2, pType, simDay, contactProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                                                // log contact if person 2 is participating in survey
                                                                LP::Contact(eventLogger, p2, p1, pType, simDay, contactProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2);
                                                                p2->RegisterContact(p1);

                                                                // transmission & infection.
                                                                // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                                                auto& h1 = p1->GetHealth();
                                                                auto& h2 = p2->GetHealth();

                                                                // if h1 infectious, account for susceptibility of p2
                                                                if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                                        if (TIC)
                                                                                h2.StopInfection();
                                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                                }

                                                                // if h2 infectious, account for susceptibility of p1
                                                                if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                                        h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                                        if (TIC)
                                                                                h1.StopInfection();
                                                                        LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                                                }
                                                        }
                                                }
                                                else {
                                                        unsigned int sampled = 0;
                                                        unsigned int good_samples = 0;

                                                        std::unordered_set<int> drawn_samples;
                                                        drawn_samples.reserve(sampleSize*2);

                                                        /*stop if:
                                                        1) drawn the required samples
                                                        2) when everyone of the interval has been picked
                                                        Number 2 is made to prevent infinite looping when less people are present in the pool than sampleSize
                                                        */
                                                        while ((good_samples < sampleSize) && (sampled < people_in_interval2)) {

                                                                int i_sampled = (int) (cHandler()*people_in_interval2) + index2;

                                                                // i_sampled has already been drawn
                                                                if (drawn_samples.find(i_sampled) != drawn_samples.end()) {
                                                                        continue;
                                                                }
                                                                
                                                                drawn_samples.insert(i_sampled);
                                                                sampled++;

                                                                // Check if member is present today
                                                                const auto p2 = pMembers[i_sampled];
                                                                if (!p2->IsInPool(pType)) {
                                                                        continue;
                                                                }
                                                                good_samples++;

                                                                // log contact if person 1 is participating in survey
                                                                LP::Contact(eventLogger, p1, p2, pType, simDay, contactProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                                                // log contact if person 2 is participating in survey
                                                                LP::Contact(eventLogger, p2, p1, pType, simDay, contactProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2);
                                                                p2->RegisterContact(p1);

                                                                // transmission & infection.
                                                                // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                                                auto& h1 = p1->GetHealth();
                                                                auto& h2 = p2->GetHealth();

                                                                // if h1 infectious, account for susceptibility of p2
                                                                if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                                        if (TIC)
                                                                                h2.StopInfection();
                                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                                }

                                                                // if h2 infectious, account for susceptibility of p1
                                                                if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                                cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                                        h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                                        if (TIC)
                                                                                h1.StopInfection();
                                                                        LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                                                }
                                                        }
                                                }
                                        }
                                }
                                index2 += pIntervalAmounts[interval2];
                        }
                        index += pIntervalAmounts[interval1];
                }
        }
        
        // Original
        else {                
                // check all contacts
                for (size_t i_person1 = 0; i_person1 < pSize; i_person1++) {
                        // check if member is present today
                        const auto p1 = pMembers[i_person1];                        
                        if (!p1->IsInPool(pType)) {
                                continue;
                        }
                        // loop over possible contacts (contacts can be initiated by each member)
                        for (size_t i_person2 = i_person1 + 1; i_person2 < pSize; i_person2++) {
                                // check if not the same person
                                if (i_person1 == i_person2) {
                                        continue;
                                }
                                // check if member is present today
                                const auto p2 = pMembers[i_person2];
                                if (!p2->IsInPool(pType)) {
                                        continue;
                                }

                                // check for contact
                                const double cProb = GetContactProbability(profile, p1, p2, pSize, pType,
                                                cnt_reduction_work, cnt_reduction_other,cnt_reduction_school,cnt_reduction_intergeneration,
                                                                        cnt_reduction_intergeneration_cutoff,population,m_cnt_intensity_householdCluster);
                                                                        
                                if (cHandler.HasContact(cProb)) {
                                        // log contact if person 1 is participating in survey
                                        LP::Contact(eventLogger, p1, p2, pType, simDay, cProb, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()));
                                        // log contact if person 2 is participating in survey
                                        LP::Contact(eventLogger, p2, p1, pType, simDay, cProb, tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()));

                                        // if track&trace is in place, option to register (both) contact(s)
                                        p1->RegisterContact(p2);
                                        p2->RegisterContact(p1);

                                        // transmission & infection.
                                        // note: no tertiary infections with TIC; so mark new case as 'recovered'
                                        auto& h1 = p1->GetHealth();
                                        auto& h2 = p2->GetHealth();

                                        // if h1 infectious, account for susceptibility of p2
                                        if (h1.IsInfectious() && h2.IsSusceptible() &&
                                                cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());
                                                        if (TIC)
                                                                        h2.StopInfection();
                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                        }

                                        // if h2 infectious, account for susceptibility of p1
                                        if (h2.IsInfectious() && h1.IsSusceptible() &&
                                                cHandler.HasTransmission(tProb * p2->GetHealth().GetRelativeTransmission(p1->GetAge()))) {
                                                        h1.StartInfection(h2.GetIdIndexCase(),p2->GetId());
                                                        if (TIC)
                                                                        h1.StopInfection();
                                                        LP::Trans(eventLogger, p2, p1, pType, simDay, h2.GetIdIndexCase());
                                        }
                                }
                        }
                }
        }
         
        auto stop = high_resolution_clock::now();

        if (false && pType == Id::PrimaryCommunity) {
                auto duration = duration_cast<microseconds>(stop - start);
                times[pSize] += duration.count();
                counts[pSize]++;
        }
        
}

//-------------------------------------------------------------------------------------------
// Definition for ContactLogMode::None and ContactLogMode::Transmission
// both with track_index_case false and true.
//-------------------------------------------------------------------------------------------
template <EventLogMode::Id LL, bool TIC>
void Infector<LL, TIC, true>::Exec(ContactPool& pool, const AgeContactProfile& profile,
                                   const TransmissionProfile& transProfile, ContactHandler& cHandler,
                                   unsigned short int simDay, shared_ptr<spdlog::logger> eventLogger,
								   double cnt_reduction_work, double cnt_reduction_other, double cnt_reduction_school,
								   double cnt_reduction_intergeneration, unsigned int cnt_reduction_intergeneration_cutoff,
								   std::shared_ptr<Population> population, double m_cnt_intensity_householdCluster,
                                                                   std::vector<long>& times, std::vector<int>& counts)
{
        using LP = LOG_POLICY<LL>;


        // check for infected members and sort
        bool   infectious_cases;
        size_t num_cases;
        tie(infectious_cases, num_cases) = pool.SortMembers();

        if (!infectious_cases) {
                return;
        }

        // set up some stuff
        const auto  pType    = pool.m_pool_type;
        const auto  pImmune  = pool.m_index_immune;
        const auto& pMembers = pool.m_members;
        const auto  pSize    = pMembers.size();
        const auto  tProb    = transProfile.GetProbability();

        // Intervals without sampling
        if(false && pSize >= 100) {          
                const auto pIntervalAmounts = pool.SortSusceptiblesByAgeIntervalsYO(num_cases);
                const auto pNumberOfIntervals = pIntervalAmounts.size();

                // Sanity check
                int counter = 0;
                for (unsigned int interval = 0; interval < pNumberOfIntervals; interval++) {
                        for (int i = 0; i < pIntervalAmounts[interval]; i++) {
                                if (!pMembers[i+counter+num_cases]->GetHealth().IsSusceptible())
                                        cout << "oei";
                        }
                        counter += pIntervalAmounts[interval];
                }
                if (counter != pImmune-num_cases)
                        cout << "Susceptible sorting is wrong" << endl;
                

                 // match infectious and susceptible members, skip last part (immune members)
                for (size_t i_infected = 0; i_infected < num_cases; i_infected++) {
                        // check if member is present today
                        const auto p1 = pMembers[i_infected];
                        if (!p1->IsInPool(pType)) {
                                continue;
                        }
                        auto& h1 = p1->GetHealth();
                        if (h1.IsInfectious()) {
                                double infected_contacts = profile[EffectiveAge(static_cast<unsigned int>(p1->GetAge()))];

                                unsigned int index = num_cases;
                                for (unsigned int interval = 0; interval < pNumberOfIntervals; interval++) {
                                        unsigned int people_in_interval = pIntervalAmounts[interval];
                                        if (people_in_interval == 0) {
                                                continue;
                                        }

                                        double interval_contacts = profile[EffectiveAge(static_cast<unsigned int>(pMembers[index]->GetAge()))];
                                        double reference_num_contacts = min(infected_contacts, interval_contacts);

                                        // initiate a contact adjustment factor, to account for physical distancing and/or contact intensity
                                        double cnt_adjustment_factor = 1;
                                        // account for physical distancing at work and in the community
                                        if(pType == Id::Workplace){
                                                cnt_adjustment_factor = (1-cnt_reduction_work);
                                        }
                                        // account for physical distancing in the community
                                        else if((pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)){
                                                // apply inter-generation distancing factor if age cutoff is > 0 and at least one age is > cutoff
                                                if((cnt_reduction_intergeneration > 0) && 
                                                ((pMembers[index]->GetAge() > cnt_reduction_intergeneration_cutoff) || (p1->GetAge() > cnt_reduction_intergeneration_cutoff))){
                                                        cnt_adjustment_factor = (1-cnt_reduction_intergeneration);

                                                } else {
                                                        // apply uniform community distancing
                                                        cnt_adjustment_factor = (1-cnt_reduction_other);
                                                }
                                        }
                                        
                                        reference_num_contacts *= cnt_adjustment_factor;
                                        double contactProb = reference_num_contacts / (pSize-1);
                                        if (contactProb >= 1) {
                                                contactProb = 0.999;
                                        }

                                        double transmissionProb = tProb * h1.GetRelativeTransmission(pMembers[index]->GetAge());
                                        
                                        for (size_t i_contact = 0; i_contact < pIntervalAmounts[interval]; i_contact++) {
                                                // Check if member is present today
                                                const auto p2 = pMembers[i_contact+index];
                                                if (!p2->IsInPool(pType)) {
                                                        continue;
                                                }

                                                auto& h2 = p2->GetHealth();
                                                // p2 has already been infected this iteration by someone in this pool
                                                if (!(h1.IsInfectious() && h2.IsSusceptible())) {
                                                        continue;
                                                }

                                                if (cHandler.HasContactAndTransmission(contactProb, transmissionProb)) {
                                                
                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());

                                                        // if track&trace is in place, option to register (both) contact(s)
                                                        p1->RegisterContact(p2); //TODO: make use of "log policy" template

                                                        // No secondary infections with TIC; just mark p2 'recovered'
                                                        if (TIC)
                                                                h2.StopInfection();
                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                }
                                        }
                                        index += pIntervalAmounts[interval];
                                }
                        }
                }
        }
        
        // Sampling (only contacts, transmissions individually)   
        else if(false && pSize >= 100) {
        //pType == Id::Workplace || pType == Id::SecondaryCommunity || pType == Id::PrimaryCommunity) {          
                const auto pIntervalAmounts = pool.SortSusceptiblesByAgeIntervalsYO(num_cases);
                const auto pNumberOfIntervals = pIntervalAmounts.size();

                std::random_device rd;
	        boost::mt19937 gen(rd());

                //const auto totalIntervalAmounts = pool.CountTotalIntervals();
                /*
                for (unsigned int interval = 0; interval < pNumberOfIntervals; interval++) {
                        cout << fakeIntervalAmounts[interval] << "-" << pIntervalAmounts[interval] << "\t";
                }
                cout << endl;
                */
                // Sanity check
                int counter = 0;
                for (unsigned int interval = 0; interval < pNumberOfIntervals; interval++) {
                        /*
                        for (int i = 0; i < pIntervalAmounts[interval]; i++) {
                                if (!pMembers[i+counter+num_cases]->GetHealth().IsSusceptible())
                                        cout << "oei";
                                cout << pMembers[i+counter+num_cases]->GetAge() << "\t";
                        }
                        cout << endl;
                        */
                        counter += pIntervalAmounts[interval];
                }
                if (counter != pImmune-num_cases)
                        cout << "Susceptible sorting is wrong" << endl;

                 // match infectious and susceptible members, skip last part (immune members)
                for (size_t i_infected = 0; i_infected < num_cases; i_infected++) {
                        // check if member is present today
                        const auto p1 = pMembers[i_infected];
                        if (!p1->IsInPool(pType)) {
                                continue;
                        }
                        auto& h1 = p1->GetHealth();
                        if (h1.IsInfectious()) {
                                double infected_contacts = profile[EffectiveAge(static_cast<unsigned int>(p1->GetAge()))];

                                unsigned int index = num_cases;
                                for (unsigned int interval = 0; interval < pNumberOfIntervals; interval++) {
                                        unsigned int people_in_interval = pIntervalAmounts[interval];
                                        if (people_in_interval == 0) {
                                                continue;
                                        }
                                        double interval_contacts = profile[EffectiveAge(static_cast<unsigned int>(pMembers[index]->GetAge()))];

                                        double reference_num_contacts = min(infected_contacts, interval_contacts);

                                        // initiate a contact adjustment factor, to account for physical distancing and/or contact intensity
                                        double cnt_adjustment_factor = 1;
                                        // account for physical distancing at work and in the community
                                        if(pType == Id::Workplace){
                                                cnt_adjustment_factor = (1-cnt_reduction_work);
                                        }
                                        // account for physical distancing in the community
                                        else if((pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)){
                                                // apply inter-generation distancing factor if age cutoff is > 0 and at least one age is > cutoff
                                                if((cnt_reduction_intergeneration > 0) && 
                                                ((pMembers[index]->GetAge() > cnt_reduction_intergeneration_cutoff) || (p1->GetAge() > cnt_reduction_intergeneration_cutoff))){
                                                        cnt_adjustment_factor = (1-cnt_reduction_intergeneration);

                                                } else {
                                                        // apply uniform community distancing
                                                        cnt_adjustment_factor = (1-cnt_reduction_other);
                                                }
                                        }
                                        
                                        reference_num_contacts *= cnt_adjustment_factor;
                                        double contactProb = reference_num_contacts / (pSize-1);

                                        //double dif = totalIntervalAmounts[interval]/pIntervalAmounts[interval];
                                        //contactProb = contactProb * dif;

                                        if (contactProb >= 1) {
                                                contactProb = 0.999;
                                        }
                                        
                                        boost::binomial_distribution<int> distr(people_in_interval, contactProb);
                                        

                                        // The number of people 1 infected will have contact with and transmit disease
                                        int sampleSize = distr(gen);
                                        /*
                                        cout << "ref_num_contacts: " << reference_num_contacts << endl;
                                        cout << "People in interval: " << people_in_interval << endl;
                                        cout << "Prob: " << contactProb << endl;
                                        cout << "Sample size: " << sampleSize << endl;
                                        cout << endl;
                                        */
                                        if (sampleSize == 0) {
                                                continue;
                                        }

                                        // Every person in the interval will be infected
                                        if (sampleSize >= people_in_interval) {
                                                for (size_t i_contact = 0; i_contact < pIntervalAmounts[interval]; i_contact++) {
                                                        // Check if member is present today
                                                        const auto p2 = pMembers[i_contact+index];
                                                        if (!p2->IsInPool(pType)) {
                                                                continue;
                                                        }

                                                        if (cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                auto& h2 = p2->GetHealth();
                                                                // p2 has already been infected this iteration by someone in this pool
                                                                if (!(h1.IsInfectious() && h2.IsSusceptible())) {
                                                                        continue;
                                                                }

                                                                h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2); //TODO: make use of "log policy" template

                                                                // No secondary infections with TIC; just mark p2 'recovered'
                                                                if (TIC)
                                                                        h2.StopInfection();
                                                                LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                        }
                                                }
                                        }
                                        else {
                                                unsigned int sampled = 0;
                                                unsigned int good_samples = 0;


                                                std::vector<int> drawn_samples(people_in_interval, -1);
                                                
                                                /*
                                                stop if:
                                                1) drawn the required samples
                                                2) when everyone of the interval has been picked
                                                Number 2 is made to prevent infinite looping when less people are present in the pool than sampleSize
                                                */
                                                while ((good_samples < sampleSize) && (drawn_samples[people_in_interval-1] == -1)) {

                                                        int i_sampled = (int) (cHandler()*people_in_interval) + index;

                                                        // i_sampled has already been drawn
                                                        if ( std::find(drawn_samples.begin(), drawn_samples.begin()+sampled, i_sampled) != drawn_samples.begin()+sampled ) {
                                                                continue;
                                                        }

                                                        drawn_samples[sampled] = i_sampled;
                                                        sampled++;


                                                        // Check if member is present today
                                                        const auto p2 = pMembers[i_sampled];
                                                        if (!p2->IsInPool(pType)) {
                                                                continue;
                                                        }

                                                        good_samples++; 

                                                        if (cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                auto& h2 = p2->GetHealth();
                                                                // p2 has already been infected this iteration by someone in this pool
                                                                if (!(h1.IsInfectious() && h2.IsSusceptible())) {
                                                                        continue;
                                                                }

                                                                h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2); //TODO: make use of "log policy" template

                                                                // No secondary infections with TIC; just mark p2 'recovered'
                                                                if (TIC)
                                                                        h2.StopInfection();
                                                                LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                        }
                                                }
                                        }
                                        index += pIntervalAmounts[interval];
                                }
                        }
                }
        }
        
        // Sampling + sorting both infectious and susceptibles (only contacts, transmissions individually)   
        else if(pSize >= 100) {
                const auto pSusceptiblesIntervalAmounts = pool.SortSusceptiblesByAgeIntervalsYO(num_cases);
                const auto pInfectiousIntervalAmounts = pool.SortInfectiousByAgeIntervalsYO(num_cases);
                const auto pNumberOfIntervals = pSusceptiblesIntervalAmounts.size();

                std::random_device rd;
                std::mt19937 gen(rd());

                //const auto totalIntervalAmounts = pool.CountTotalIntervals();

                // Sanity check
                /*
                int counter = 0;
                for (unsigned int interval = 0; interval < pNumberOfIntervals; interval++) {
                        for (int i = 0; i < pIntervalAmounts[interval]; i++) {
                                if (!pMembers[i+counter+num_cases]->GetHealth().IsSusceptible())
                                        cout << "error";
                                cout << pMembers[i+counter+num_cases]->GetAge() << "\t";
                        }
                        cout << endl;
                        counter += pIntervalAmounts[interval];
                }
                if (counter != pImmune-num_cases)
                        cout << "Susceptible sorting is wrong" << endl;
                */
                
                int index1 = 0;
                for (int interval1 = 0; interval1 < pNumberOfIntervals; interval1++) {
                        if (pInfectiousIntervalAmounts[interval1 == 0]) {
                                continue;
                        }
                        unsigned int people_in_interval1 = pInfectiousIntervalAmounts[interval1];
                        double inf_ref_num_contacts = profile[EffectiveAge(static_cast<unsigned int>(pMembers[index1]->GetAge()))];

                        int index2 = num_cases;
                        for (int interval2 = 0; interval2  < pNumberOfIntervals; interval2++) {
                                if (pSusceptiblesIntervalAmounts[interval2] == 0) {
                                        continue;
                                }
                                unsigned int people_in_interval2 = pSusceptiblesIntervalAmounts[interval2];

                                double sus_ref_num_contacts = profile[EffectiveAge(static_cast<unsigned int>(pMembers[index2]->GetAge()))];
                                double reference_num_contacts = min(inf_ref_num_contacts, sus_ref_num_contacts);

                                double contactProb = CustomGetContactProbability(reference_num_contacts, pSize, pType,
                                                                EffectiveAge(static_cast<unsigned int>(pMembers[index1]->GetAge())),
                                                                EffectiveAge(static_cast<unsigned int>(pMembers[index2]->GetAge())),
                                                                cnt_reduction_work, cnt_reduction_intergeneration, cnt_reduction_other,
                                                                cnt_reduction_intergeneration_cutoff);
                                
                                std::binomial_distribution<int> distr(people_in_interval2, contactProb);
                                
                                // Iterate over all the infectious in interval1
                                for (size_t i_infected = 0; i_infected < pInfectiousIntervalAmounts[interval1]; i_infected++) {
                                        const auto p1 = pMembers[i_infected+index1];
                                        if (!p1->IsInPool(pType)) {
                                                continue;
                                        }
                                        auto& h1 = p1->GetHealth();

                                        int sampleSize = distr(gen);
                                        /*
                                        cout << "ref_num_contacts: " << reference_num_contacts << endl;
                                        cout << "People in interval: " << people_in_interval << endl;
                                        cout << "Prob: " << contactProb << endl;
                                        cout << "Sample size: " << sampleSize << endl;
                                        cout << endl;
                                        */
                                        if (sampleSize == 0) {
                                                continue;
                                        }
                                        if (sampleSize >= people_in_interval2) {
                                                for (size_t i_susceptible = 0; i_susceptible < pSusceptiblesIntervalAmounts[interval2]; i_susceptible++) {
                                                        // Check if member is present today
                                                        const auto p2 = pMembers[i_susceptible+index2];
                                                        if (!p2->IsInPool(pType)) {
                                                                continue;
                                                        }

                                                        if (cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                auto& h2 = p2->GetHealth();
                                                                // p2 has already been infected this iteration by someone in this pool
                                                                if (!(h1.IsInfectious() && h2.IsSusceptible())) {
                                                                        continue;
                                                                }

                                                                h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2); //TODO: make use of "log policy" template

                                                                // No secondary infections with TIC; just mark p2 'recovered'
                                                                if (TIC)
                                                                        h2.StopInfection();
                                                                LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                        }
                                                }
                                        }
                                        else {
                                                unsigned int sampled = 0;
                                                unsigned int good_samples = 0;


                                                std::vector<int> drawn_samples(people_in_interval2, -1);
                                                
                                                /*
                                                stop if:
                                                1) drawn the required samples
                                                2) when everyone of the interval has been picked
                                                Number 2 is made to prevent infinite looping when less people are present in the pool than sampleSize
                                                */
                                                while ((good_samples < sampleSize) && (drawn_samples[people_in_interval2-1] == -1)) {

                                                        int i_sampled = (int) (cHandler()*people_in_interval2) + index2;

                                                        // i_sampled has already been drawn
                                                        if ( std::find(drawn_samples.begin(), drawn_samples.begin()+sampled, i_sampled) != drawn_samples.begin()+sampled ) {
                                                                continue;
                                                        }

                                                        drawn_samples[sampled] = i_sampled;
                                                        sampled++;


                                                        // Check if member is present today
                                                        const auto p2 = pMembers[i_sampled];
                                                        if (!p2->IsInPool(pType)) {
                                                                continue;
                                                        }

                                                        good_samples++; 

                                                        if (cHandler.HasTransmission(tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                                auto& h2 = p2->GetHealth();
                                                                // p2 has already been infected this iteration by someone in this pool
                                                                if (!(h1.IsInfectious() && h2.IsSusceptible())) {
                                                                        continue;
                                                                }

                                                                h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());

                                                                // if track&trace is in place, option to register (both) contact(s)
                                                                p1->RegisterContact(p2); //TODO: make use of "log policy" template

                                                                // No secondary infections with TIC; just mark p2 'recovered'
                                                                if (TIC)
                                                                        h2.StopInfection();
                                                                LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                        }
                                                }
                                        }
                                }
                                index2 += pSusceptiblesIntervalAmounts[interval2];
                        }
                        index1 += pInfectiousIntervalAmounts[interval1];
                }
        }

        // Sampling (the one that gives the wrong results)
        else if(false && pSize >= 100) {          
                const auto pIntervalAmounts = pool.SortSusceptiblesByAgeIntervalsYO(num_cases);
                const auto pNumberOfIntervals = pIntervalAmounts.size();

                std::random_device rd;
                std::mt19937 gen(rd());

                 // match infectious and susceptible members, skip last part (immune members)
                for (size_t i_infected = 0; i_infected < num_cases; i_infected++) {
                        // check if member is present today
                        const auto p1 = pMembers[i_infected];
                        if (!p1->IsInPool(pType)) {
                                continue;
                        }
                        auto& h1 = p1->GetHealth();
                        if (h1.IsInfectious()) {
                                double infected_contacts = profile[EffectiveAge(static_cast<unsigned int>(p1->GetAge()))];

                                unsigned int index = num_cases;
                                for (unsigned int interval = 0; interval < pNumberOfIntervals; interval++) {
                                        unsigned int people_in_interval = pIntervalAmounts[interval];
                                        if (people_in_interval == 0) {
                                                continue;
                                        }

                                        double interval_contacts = profile[EffectiveAge(static_cast<unsigned int>(pMembers[index]->GetAge()))];

                                        double reference_num_contacts = min(infected_contacts, interval_contacts);

                                        // initiate a contact adjustment factor, to account for physical distancing and/or contact intensity
                                        double cnt_adjustment_factor = 1;
                                        // account for physical distancing at work and in the community
                                        if(pType == Id::Workplace){
                                                cnt_adjustment_factor = (1-cnt_reduction_work);
                                        }
                                        // account for physical distancing in the community
                                        else if((pType == Id::PrimaryCommunity || pType == Id::SecondaryCommunity)){
                                                // apply inter-generation distancing factor if age cutoff is > 0 and at least one age is > cutoff
                                                if((cnt_reduction_intergeneration > 0) && 
                                                ((pMembers[index]->GetAge() > cnt_reduction_intergeneration_cutoff) || (p1->GetAge() > cnt_reduction_intergeneration_cutoff))){
                                                        cnt_adjustment_factor = (1-cnt_reduction_intergeneration);

                                                } else {
                                                        // apply uniform community distancing
                                                        cnt_adjustment_factor = (1-cnt_reduction_other);
                                                }
                                        }
                                        
                                        reference_num_contacts *= cnt_adjustment_factor;
                                        double contactProb = reference_num_contacts / (pSize-1);
                                        contactProb *= 2;
                                        if (contactProb >= 1) {
                                                contactProb = 0.999;
                                        }

                                        double transmissionProb = tProb * h1.GetRelativeTransmission(pMembers[index]->GetAge());
                                        double prob = contactProb * transmissionProb;
                                        
                                        binomial_distribution<int> distr(people_in_interval, prob);

                                        // The number of people 1 infected will have contact with and transmit disease
                                        int sampleSize = distr(gen);
                                        if (sampleSize == 0) {
                                                continue;
                                        }

                                        // Every person in the interval will be infected
                                        if (sampleSize >= people_in_interval) {
                                                for (size_t i_contact = 0; i_contact < pIntervalAmounts[interval]; i_contact++) {
                                                        // Check if member is present today
                                                        const auto p2 = pMembers[i_contact+index];
                                                        if (!p2->IsInPool(pType)) {
                                                                continue;
                                                        }

                                                        auto& h2 = p2->GetHealth();
                                                        // p2 has already been infected this iteration by someone in this pool
                                                        if (!(h1.IsInfectious() && h2.IsSusceptible())) {
                                                                continue;
                                                        }

                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());

                                                        // if track&trace is in place, option to register (both) contact(s)
                                                        p1->RegisterContact(p2); //TODO: make use of "log policy" template

                                                        // No secondary infections with TIC; just mark p2 'recovered'
                                                        if (TIC)
                                                                h2.StopInfection();
                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                }
                                        }
                                        else {
                                                unsigned int sampled = 0;
                                                unsigned int good_samples = 0;


                                                std::vector<int> drawn_samples(people_in_interval, -1);
                                                
                                                /*
                                                stop if:
                                                1) drawn the required samples
                                                2) when everyone of the interval has been picked
                                                Number 2 is made to prevent infinite looping when less people are present in the pool than sampleSize
                                                */
                                                while ((good_samples < sampleSize) && (drawn_samples[people_in_interval-1] == -1)) {

                                                        int i_sampled = (int) (cHandler()*people_in_interval) + index;

                                                        // i_sampled has already been drawn
                                                        if ( std::find(drawn_samples.begin(), drawn_samples.begin()+sampled, i_sampled) != drawn_samples.begin()+sampled ) {
                                                                continue;
                                                        }

                                                        drawn_samples[sampled] = i_sampled;
                                                        sampled++;

                                                        good_samples++; 

                                                        // Check if member is present today
                                                        const auto p2 = pMembers[i_sampled];
                                                        if (!p2->IsInPool(pType)) {
                                                                continue;
                                                        }

                                                        auto& h2 = p2->GetHealth();
                                                        // p2 has already been infected this iteration by someone in this pool
                                                        if (!(h1.IsInfectious() && h2.IsSusceptible())) {
                                                                continue;
                                                        }

                                                        
                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());

                                                        // if track&trace is in place, option to register (both) contact(s)
                                                        p1->RegisterContact(p2); //TODO: make use of "log policy" template

                                                        // No secondary infections with TIC; just mark p2 'recovered'
                                                        if (TIC)
                                                                h2.StopInfection();
                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                }
                                        }
                                        index += pIntervalAmounts[interval];
                                }
                        }
                }
        }
        
        // Original
        else { 
                // match infectious and susceptible members, skip last part (immune members)
                for (size_t i_infected = 0; i_infected < num_cases; i_infected++) {
                        // check if member is present today
                        const auto p1 = pMembers[i_infected];
                        if (!p1->IsInPool(pType)) {
                                continue;
                        }
                        auto& h1 = p1->GetHealth();
                        if (h1.IsInfectious()) {
                                // loop over possible susceptible contacts
                                for (size_t i_contact = num_cases; i_contact < pImmune; i_contact++) {
                                        // check if member is present today
                                        const auto p2 = pMembers[i_contact];
                                        if (!p2->IsInPool(pType)) {
                                                continue;
                                        }
                                        const double cProb_p1 = GetContactProbability(profile, p1, p2, pSize, pType,
                                                        cnt_reduction_work, cnt_reduction_other,cnt_reduction_school, cnt_reduction_intergeneration,
                                                                                        cnt_reduction_intergeneration_cutoff,population,m_cnt_intensity_householdCluster);
                                        if (cHandler.HasContactAndTransmission(cProb_p1, tProb * p1->GetHealth().GetRelativeTransmission(p2->GetAge()))) {
                                                auto& h2 = p2->GetHealth();
                                                if (h1.IsInfectious() && h2.IsSusceptible()) {
                                                        h2.StartInfection(h1.GetIdIndexCase(),p1->GetId());

                                                        // if track&trace is in place, option to register (both) contact(s)
                                                        p1->RegisterContact(p2); //TODO: make use of "log policy" template

                                                        // No secondary infections with TIC; just mark p2 'recovered'
                                                        if (TIC)
                                                                h2.StopInfection();
                                                        LP::Trans(eventLogger, p1, p2, pType, simDay, h1.GetIdIndexCase());
                                                }
                                        }
                                }
                        }
                }
        }
}

//--------------------------------------------------------------------------
// All explicit instantiations.
//--------------------------------------------------------------------------
template class Infector<EventLogMode::Id::None, false>;
template class Infector<EventLogMode::Id::None, true>;
template class Infector<EventLogMode::Id::Transmissions, false>;
template class Infector<EventLogMode::Id::Transmissions, true>;
template class Infector<EventLogMode::Id::All, false>;
template class Infector<EventLogMode::Id::All, true>;


} // namespace stride
