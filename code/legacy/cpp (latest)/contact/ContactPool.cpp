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
 *  Copyright 2019, Kuylen E, Willem L, Broeckhove J
 */

/**
 * @file
 * Implementation for the core ContcatPool class.
 */

#include "ContactPool.h"

#include "pop/Age.h"
#include "pop/Person.h"

#include <algorithm>

namespace stride {

using namespace std;

const int ContactPool::workplace_interval_ages[] = {18, 65, 120};
const int ContactPool::community_interval_ages[] = {3, 6, 12, 18, 23, 45, 65, 75, 120};

const int ContactPool::workplace_interval_ages2[] = {0, 18, 65};
const int ContactPool::community_interval_ages2[] = {0, 3, 6, 12, 18, 23, 45, 65, 75};

ContactPool::ContactPool(unsigned int poolId, ContactType::Id type)
    : m_index_immune(0), m_pool_id(poolId), m_pool_type(type), m_members(), m_has_infant(false)
{
}

void ContactPool::AddMember(Person* p)
{
        m_members.emplace_back(p);
        m_index_immune++;

        if(p->GetAge()<1){
        	m_has_infant = true;
        }
}

unsigned int ContactPool::GetInfectedCount() const
{
        unsigned int infected = 0;

        for (stride::Person* person : m_members) {
                if (person->GetHealth().IsInfected()) {
                        infected++;
                }
        }
        return infected;
}

std::tuple<bool, unsigned int> ContactPool::SortMembers()
{
        bool         infectious_cases = false;
        unsigned int num_cases        = 0;

        for (size_t i_member = 0; i_member < m_index_immune; i_member++) {
                // if immune, move to back
                if (m_members[i_member]->GetHealth().IsImmune()) {
                        bool         swapped   = false;
                        unsigned int new_place = m_index_immune - 1;
                        m_index_immune--;
                        while (!swapped && new_place > i_member) {
                                if (m_members[new_place]->GetHealth().IsImmune()) {
                                        m_index_immune--;
                                        new_place--;
                                } else {
                                        swap(m_members[i_member], m_members[new_place]);
                                        swapped = true;
                                }
                        }
                }
                // else, if not susceptible, move to front
                else if (!m_members[i_member]->GetHealth().IsSusceptible()) {
                        if (!infectious_cases && m_members[i_member]->GetHealth().IsInfectious()) {
                                infectious_cases = true;
                        }
                        if (i_member > num_cases) {
                                swap(m_members[i_member], m_members[num_cases]);
                        }
                        num_cases++;
                }
        }
        return std::make_tuple(infectious_cases, num_cases);
}

std::vector<unsigned int> ContactPool::SortSusceptiblesByAgeIntervalsYO(unsigned int num_cases)
{
        unsigned int amount_intervals;
        const int *age_intervals;

        if (m_pool_type == ContactType::Id::Workplace) {
                amount_intervals = sizeof(workplace_interval_ages)/sizeof(workplace_interval_ages[0]);
                age_intervals = workplace_interval_ages;
        }
        else if (m_pool_type == ContactType::Id::PrimaryCommunity || m_pool_type == ContactType::Id::SecondaryCommunity) {
                amount_intervals = sizeof(community_interval_ages)/sizeof(community_interval_ages[0]);
                age_intervals = community_interval_ages;
        }
        else
        {
                std::cerr << "Error" << endl;
        }

        std::vector<unsigned int> interval_counters(amount_intervals, 0);

        size_t poolsize = m_members.size();
        size_t index = num_cases;

        for (unsigned int interval = 0; interval < amount_intervals; interval++) {
                for (size_t i_member = index; i_member < m_index_immune; i_member++) {
                        if (EffectiveAge(static_cast<unsigned int>(m_members[i_member]->GetAge())) < age_intervals[interval]) {
                                if (i_member != index)
                                {
                                        swap(m_members[i_member], m_members[index]);
                                }
                                index++;
                                interval_counters[interval]++;
                        }
                }
        }

        return interval_counters;
}

std::vector<unsigned int> ContactPool::SortInfectiousByAgeIntervalsYO(unsigned int num_cases)
{
        unsigned int amount_intervals;
        const int *age_intervals;

        if (m_pool_type == ContactType::Id::Workplace) {
                amount_intervals = sizeof(workplace_interval_ages)/sizeof(workplace_interval_ages[0]);
                age_intervals = workplace_interval_ages;
        }
        else if (m_pool_type == ContactType::Id::PrimaryCommunity || m_pool_type == ContactType::Id::SecondaryCommunity) {
                amount_intervals = sizeof(community_interval_ages)/sizeof(community_interval_ages[0]);
                age_intervals = community_interval_ages;
        }
        else
        {
                std::cerr << "Error" << endl;
        }

        std::vector<unsigned int> interval_counters(amount_intervals, 0);

        size_t poolsize = m_members.size();
        size_t index = 0;

        for (unsigned int interval = 0; interval < amount_intervals; interval++) {
                for (size_t i_member = index; i_member < num_cases; i_member++) {
                        if (m_members[i_member]->GetHealth().IsInfectious() &&
                        (EffectiveAge(static_cast<unsigned int>(m_members[i_member]->GetAge())) < age_intervals[interval])) {
                                if (i_member != index)
                                {
                                        swap(m_members[i_member], m_members[index]);
                                }
                                index++;
                                interval_counters[interval]++;
                        }
                }
        }

        return interval_counters;
}

std::vector<unsigned int> ContactPool::SortMembersByAgeIntervalsYO()
{
        unsigned int amount_intervals;
        const int *age_intervals;

        if (m_pool_type == ContactType::Id::Workplace) {
                amount_intervals = sizeof(workplace_interval_ages)/sizeof(workplace_interval_ages[0]);
                age_intervals = workplace_interval_ages;
        }
        else if (m_pool_type == ContactType::Id::PrimaryCommunity || m_pool_type == ContactType::Id::SecondaryCommunity) {
                amount_intervals = sizeof(community_interval_ages)/sizeof(community_interval_ages[0]);
                age_intervals = community_interval_ages;
        }
        else
        {
                std::cerr << "Error" << endl;
        }

        std::vector<unsigned int> interval_counters(amount_intervals, 0);

        size_t poolsize = m_members.size();
        size_t index = 0;

        for (unsigned int interval = 0; interval < amount_intervals; interval++) {
                for (size_t i_member = index; i_member < poolsize; i_member++) {
                        if (EffectiveAge(static_cast<unsigned int>(m_members[i_member]->GetAge())) < age_intervals[interval]) {
                                if (i_member != index)
                                {
                                        swap(m_members[i_member], m_members[index]);
                                }
                                index++;
                                interval_counters[interval]++;
                        }
                }
        }

        return interval_counters;
}

std::vector<unsigned int> ContactPool::SortMembersByAgeIntervalsOY()
{
        unsigned int amount_intervals;
        const int *age_intervals;
        
        if (m_pool_type == ContactType::Id::Workplace) {
                amount_intervals = sizeof(workplace_interval_ages2)/sizeof(workplace_interval_ages2[0]);
                age_intervals = workplace_interval_ages2;
        }
        else if (m_pool_type == ContactType::Id::PrimaryCommunity || m_pool_type == ContactType::Id::SecondaryCommunity) {
                amount_intervals = sizeof(community_interval_ages2)/sizeof(community_interval_ages2[0]);
                age_intervals = community_interval_ages2;
        }
        else
        {
                std::cerr << "Error" << endl;
        }
        
        std::vector<unsigned int> interval_counters(amount_intervals, 0);

        size_t poolsize = m_members.size();
        size_t index = 0;

        // Van oud naar jong
        for (unsigned int interval = 0; interval < amount_intervals; interval++) {
                for (size_t i_member = index; i_member < poolsize; i_member++) {
                        if (EffectiveAge(static_cast<unsigned int>(m_members[i_member]->GetAge())) >= age_intervals[amount_intervals-1-interval]) {
                                if (i_member != index)
                                {
                                        swap(m_members[i_member], m_members[index]);
                                }
                                index++;
                                interval_counters[interval]++;
                        }
                }
        }
        return interval_counters;
}

std::vector<unsigned int> ContactPool::CountTotalIntervals()
{
        unsigned int amount_intervals;
        const int *age_intervals;

        if (m_pool_type == ContactType::Id::Workplace) {
                amount_intervals = sizeof(workplace_interval_ages)/sizeof(workplace_interval_ages[0]);
                age_intervals = workplace_interval_ages;
        }
        else if (m_pool_type == ContactType::Id::PrimaryCommunity || m_pool_type == ContactType::Id::SecondaryCommunity) {
                amount_intervals = sizeof(community_interval_ages)/sizeof(community_interval_ages[0]);
                age_intervals = community_interval_ages;
        }
        else
        {
                std::cerr << "Error" << endl;
        }
        size_t poolsize = m_members.size();

        std::vector<unsigned int> interval_counters(amount_intervals, 0);
        std::vector<bool> already_counted(poolsize, false);


        for (unsigned int interval = 0; interval < amount_intervals; interval++) {
                for (size_t i_member = 0; i_member < poolsize; i_member++) {
                        if (EffectiveAge(static_cast<unsigned int>(m_members[i_member]->GetAge())) < age_intervals[interval]) {
                                if (!already_counted[i_member]) {
                                        already_counted[i_member] = true;
                                        interval_counters[interval]++;
                                }
                        }
                }
        }

        return interval_counters;
}

unsigned int ContactPool::PeopleInPool() {
        unsigned int people_in_pool = 0;

        for (size_t i_member = 0; i_member < m_members.size(); i_member++) {
                if (m_members[i_member]->IsInPool(m_pool_type))
                        people_in_pool++;
        }

        return people_in_pool;
}

} // namespace stride
