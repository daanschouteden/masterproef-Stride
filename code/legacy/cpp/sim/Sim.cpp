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
 *  Copyright 2020, Kuylen E, Willem L, Broeckhove J
 */

/**
 * @file
 * Implementation for the Simulator class.
 */

#include "Sim.h"

#include "calendar/Calendar.h"
#include "contact/ContactType.h"
#include "contact/InfectorExec.h"
#include "disease/DiseaseSeeder.h"
#include "pop/Population.h"
#include "sim/SimBuilder.h"
#include "util/RunConfigManager.h"

#include <omp.h>
#include <utility>


#include <chrono>
using namespace std::chrono; 

#include <algorithm>    // std::shuffle
#include <iostream>
#include <random>

#include <fstream>
#include <iostream>

using namespace std;

namespace stride {

using namespace std;
using namespace util;
using namespace EventLogMode;

Sim::Sim()
    : m_config(), m_event_log_mode(Id::None), m_num_threads(1U), m_track_index_case(false),
      m_calendar(nullptr), m_contact_profiles(), m_handlers(), m_infector_default(),m_infector_tracing(),
      m_population(nullptr), m_rn_man(), m_transmission_profile(), m_cnt_reduction_workplace(0), m_cnt_reduction_other(0),
	  m_cnt_reduction_workplace_exit(0),m_cnt_reduction_other_exit(0), m_cnt_reduction_school_exit(0), m_cnt_reduction_intergeneration(0),
	  m_cnt_reduction_intergeneration_cutoff(0), m_compliance_delay_workplace(0), m_compliance_delay_other(0),
	  m_day_of_community_distancing(0), m_day_of_workplace_distancing(0), m_day_of_community_distancing_exit(0),m_cnt_intensity_householdCluster(0),
      m_is_isolated_from_household(false),
	  m_public_health_agency(),m_universal_testing(),m_num_daily_imported_cases(0)

{
}

std::shared_ptr<Sim> Sim::Create(const boost::property_tree::ptree& config, shared_ptr<Population> pop,
                                 util::RnMan rnMan)
{
        struct make_shared_enabler : public Sim
        {
                explicit make_shared_enabler() : Sim() {}
        };
        shared_ptr<Sim> sim = make_shared<make_shared_enabler>();
        SimBuilder(config).Build(sim, std::move(pop), std::move(rnMan));
        return sim;
}

void Sim::TimeStep(string& first, string& second, string& third,
				string& household, string& k12school, string& college, string& workplace, string& primary, string& secondary, string& cluster, bool measure)
{
	// Logic where you compute (on the basis of input/config for initial day or on the basis of
	// number of sick persons, duration of epidemic etc) what kind of DaysOff scheme you apply.
	const bool isRegularWeekday     = m_calendar->IsRegularWeekday();
	const bool isWorkplaceDistancingEnforced   = m_calendar->IsWorkplaceDistancingEnforced();
	const bool isCommunityDistancingEnforced   = m_calendar->IsCommunityDistancingEnforced();
	const bool isHouseholdClusteringAllowed    = m_calendar->IsHouseholdClusteringAllowed();

//        // skip all K12 schools?
//        bool areAllK12SchoolsOff = (m_calendar->IsSchoolClosed(1) && m_calendar->IsSchoolClosed(6) && m_calendar->IsSchoolClosed(11));
//        bool isCollegeOff   = m_calendar->IsSchoolClosed(22);

//        std::cout <<
//        		isRegularWeekday << " " <<
//				isWorkplaceDistancingEnforced << " " <<
//				isCommunityDistancingEnforced << " " <<
//				m_calendar->IsContactTracingActivated() << " " <<
//				isHouseholdClusteringAllowed << " " << endl;


	// increment the number of days in lock-down and account for compliance
	double workplace_distancing_factor = 0.0;
	if(isWorkplaceDistancingEnforced){
		m_day_of_workplace_distancing += 1;

		workplace_distancing_factor = m_cnt_reduction_workplace;

		if(m_day_of_workplace_distancing < m_compliance_delay_workplace){
			workplace_distancing_factor *= 1.0 * m_day_of_workplace_distancing / m_compliance_delay_workplace;
		}
	} else if(m_day_of_workplace_distancing > 0){
		workplace_distancing_factor = m_cnt_reduction_workplace_exit;
	}

		// increment the number of days in lock-down and account for compliance
	double community_distancing_factor = 0.0;
	double intergeneration_distancing_factor = 0.0;
	if(isCommunityDistancingEnforced){
		m_day_of_community_distancing += 1;

		community_distancing_factor = m_cnt_reduction_other;
		intergeneration_distancing_factor = m_cnt_reduction_intergeneration;

		if(m_day_of_community_distancing < m_compliance_delay_other){
			community_distancing_factor *= 1.0 * m_day_of_community_distancing / m_compliance_delay_other;
		}
	} else if (m_day_of_community_distancing > 0){

		community_distancing_factor       = m_cnt_reduction_other_exit;
		intergeneration_distancing_factor = m_cnt_reduction_intergeneration;
	}

	// get distancing at school
	double school_distancing_factor = (m_day_of_workplace_distancing > 0) ? m_cnt_reduction_school_exit : 0 ;

	// To be used in update of population & contact pools.
	Population& population    = *m_population;
	auto&       logger        = population.RefEventLogger();
	auto&       poolSys       = population.RefPoolSys();
	auto        eventLogger   = population.RefEventLogger();
	const auto  simDay        = m_calendar->GetSimulationDay();

	// Select infector, based on tracing
	const auto& infector      = m_public_health_agency.IsContactTracingActive(m_calendar) ? *m_infector_tracing : *m_infector_default;

	// set HouseholdCluster intensity
	double cnt_intensity_householdCluster = 0.0;
	if (isHouseholdClusteringAllowed && poolSys.RefPools(ContactType::Id::HouseholdCluster).size() > 1){
		cnt_intensity_householdCluster = m_cnt_intensity_householdCluster;
	}

	// Import infected cases into the population
	if(m_calendar->GetNumberOfImportedCases() > 0){
		DiseaseSeeder(m_config, m_rn_man).ImportInfectedCases(m_population, m_calendar->GetNumberOfImportedCases(), simDay);
	// cout << "import cases: " << m_calendar->GetNumberOfImportedCases() << endl;
		logger->info("[IMPORT-CASES] sim_day={} count={}", simDay, m_calendar->GetNumberOfImportedCases());        	
	}

	auto start1 = high_resolution_clock::now(); 

	#pragma omp parallel num_threads(m_num_threads)
	{
		const auto thread_num = static_cast<unsigned int>(omp_get_thread_num());
		// Update health status and presence/absence in contact pools
		// depending on health status, work/school day and whether
		// we want to track index cases without adaptive behavior
		#pragma omp for schedule(static)
		for (size_t i = 0; i < population.size(); ++i) {

			// adjust K12SchoolOff boolean to school type for individual 'i'
			//	bool isK12SchoolOff = m_public_health_agency.IsK12SchoolOff(population[i].GetAge(),
			//	m_calendar->IsSchoolClosed(0), //isPreSchoolOff,
			//	m_calendar->IsSchoolClosed(6), //isPrimarySchoolOff,
			//	m_calendar->IsSchoolClosed(11), //isSecondarySchoolOff,
			//	m_calendar->IsSchoolClosed(20)); //isCollegeOff);

			bool isK12SchoolOff = m_calendar->IsSchoolClosed(population[i].GetAge());
			bool isCollegeOff   = m_calendar->IsSchoolClosed(population[i].GetAge());
			// update health and presence at different contact pools
			population[i].Update(isRegularWeekday, isK12SchoolOff, isCollegeOff,
					isWorkplaceDistancingEnforced, isHouseholdClusteringAllowed,
					m_is_isolated_from_household,
					m_handlers[thread_num], 
					m_calendar);
		}
	}// end pragma openMP
	auto stop1 = high_resolution_clock::now();
	auto duration1 = duration_cast<microseconds>(stop1 - start1); 
	first.append(to_string(duration1.count()) + "\n");

	auto start2 = high_resolution_clock::now(); 

		// Perform contact tracing (if activated)
		m_public_health_agency.PerformContactTracing(m_population, m_handlers[0], m_calendar);

	auto stop2 = high_resolution_clock::now();
	auto duration2 = duration_cast<microseconds>(stop2 - start2); 
	second.append(to_string(duration2.count()) + "\n");

		// Perform universal testing 
		m_universal_testing.PerformUniversalTesting(m_population, m_handlers[0], m_calendar,m_public_health_agency);

	
	std::vector<long> times(1501, 0);
	std::vector<int> counts(1501, 0);

	auto start3 = high_resolution_clock::now();   

	std::random_device rd;
	std::mt19937 gen(rd());

	for (auto typ : ContactType::IdList) {
		if ((typ == ContactType::Id::Workplace && !isRegularWeekday) ||
			(typ == ContactType::Id::K12School && !isRegularWeekday) ||
			(typ == ContactType::Id::College && !isRegularWeekday) ||
			(typ == ContactType::Id::HouseholdCluster && !isHouseholdClusteringAllowed)) {
				continue;
		}
		/*
		if (typ == ContactType::Id::Household)
			printf("Household\n");
		else if (typ == ContactType::Id::K12School)
			printf("K12School\n");
		else if (typ == ContactType::Id::College)
			printf("College\n");
		else if (typ == ContactType::Id::Workplace)
			printf("Workplace\n");
		else if (typ == ContactType::Id::PrimaryCommunity)
			printf("Primary\n");
		else if (typ == ContactType::Id::SecondaryCommunity)
			printf("Secondary\n");
		else if (typ == ContactType::Id::HouseholdCluster)
			printf("Cluster\n");
		*/
		
		auto start4 = high_resolution_clock::now();

		#pragma omp parallel num_threads(m_num_threads)
		{
			const auto thread_num = static_cast<unsigned int>(omp_get_thread_num());
			// Infector updates individuals for contacts & transmission within each pool.
			// Skip pools with id = 0, because it means Not Applicable.

			#pragma omp for schedule(static)
			for (size_t i = 1; i < poolSys.RefPools(typ).size(); i++) { // NOLINT
					infector(poolSys.RefPools(typ)[i], m_contact_profiles[typ], m_transmission_profile,
								m_handlers[thread_num], simDay, eventLogger,
								workplace_distancing_factor,
								community_distancing_factor,
								school_distancing_factor,
								intergeneration_distancing_factor,m_cnt_reduction_intergeneration_cutoff,
								m_population,cnt_intensity_householdCluster, times, counts, gen);
			}
		}

		auto stop4 = high_resolution_clock::now();
		auto duration4 = duration_cast<microseconds>(stop4 - start4);
		if (typ == ContactType::Id::Household)
			household.append(to_string(duration4.count()));
		else if (typ == ContactType::Id::K12School)
			k12school.append(to_string(duration4.count()));
		else if (typ == ContactType::Id::College)
			college.append(to_string(duration4.count()));
		else if (typ == ContactType::Id::Workplace)
			workplace.append(to_string(duration4.count()));
		else if (typ == ContactType::Id::PrimaryCommunity)
			primary.append(to_string(duration4.count()));
		else if (typ == ContactType::Id::SecondaryCommunity)
			secondary.append(to_string(duration4.count()));
		else if (typ == ContactType::Id::HouseholdCluster)
			cluster.append(to_string(duration4.count()));
	}

	auto stop3 = high_resolution_clock::now();
	auto duration3 = duration_cast<microseconds>(stop3 - start3); 
	third.append(to_string(duration3.count()) + "\n");

	if (measure) {
		cout << "writing out times.txt" << endl;
		ofstream fstr;
		fstr.open("times.txt", ios::out);
		for (int i = 0; i < times.size(); i++) {
			if (counts[i] != 0)
				fstr << times[i] / counts[i] << endl;
			else
				fstr << endl;
		}
		fstr.close();
	}

	household.append("\n");
	k12school.append("\n");
	college.append("\n");
	workplace.append("\n");
	primary.append("\n");
	secondary.append("\n");
	cluster.append("\n");

	m_population->RefEventLogger()->flush();
	m_calendar->AdvanceDay();
}

} // namespace stride
