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
 *  Copyright 2017, 2018, Kuylen E, Willem L, Broeckhove J
 */

/**
 * @file
 * Implementation for SimRunner.
 */

#include "SimRunner.h"

#include "calendar/Calendar.h"
#include "pop/Population.h"
#include "sim/Sim.h"

#include <fstream>
#include <iostream>

using namespace stride::sim_event;
using namespace boost::property_tree;
using namespace std;

namespace stride {

SimRunner::SimRunner(const ptree& configPt, shared_ptr<Sim> sim)
    : m_clock("total_clock"), m_config(configPt), m_sim(std::move(sim))
{
        Notify(Id::SetupBegin);
        m_clock.Start();
        Notify(Id::SetupEnd);
}

void SimRunner::Run(unsigned int numSteps)
{
        string first="", second="", third="", total="", household="", k12school="", college="", workplace="", primary="", secondary="", cluster="";

	std::random_device rd;
	std::mt19937 gen(rd());

        // Saveguard against repeatedly firing AtStart, so bypass if numSteps == 0.
        if (numSteps != 0U) {
                // Prelims.
                m_clock.Start();
                const auto numDays = m_config.get<unsigned int>("run.num_days");

                // We are AtStart: no steps have taken yet, so signal AtStart.
                if (m_sim->GetCalendar()->GetSimulationDay() == 0) {
                        Notify(Id::AtStart);
                }

                // Take numSteps but do not go beyond numDays.
                for (unsigned int i = 0; i < numSteps; i++) {
                        // We are AtStart: no steps have taken yet, so signal AtStart.
                        if (m_sim->GetCalendar()->GetSimulationDay() == 0) {
                                m_sim->TimeStep(first, second, third, total, household, k12school, college, workplace, primary, secondary, cluster, true, gen);
                                Notify(Id::Stepped);
                        }
                        // This is not the last step: execute and signal Stepped.
                        else if (m_sim->GetCalendar()->GetSimulationDay() < numDays - 1) {
                                m_sim->TimeStep(first, second, third, total, household, k12school, college, workplace, primary, secondary, cluster, false, gen);
                                Notify(Id::Stepped);
                                // This is the last step so execute and afterwards signal Stepped and Finished
                        } else if (m_sim->GetCalendar()->GetSimulationDay() == numDays - 1) {
                                m_sim->TimeStep(first, second, third, total, household, k12school, college, workplace, primary, secondary, cluster, false, gen);
                                Notify(Id::Stepped);
                                Notify(Id::Finished);
                                break;
                                // We are apparently already at the end of the numDays so nothing to do or signal.
                        } else {
                                break;
                        }
                }

                m_clock.Stop();
        }
        ofstream fstr;
        fstr.open("first.txt", ios::out);
        fstr << first << endl;
        fstr.close();
        fstr.open("second.txt", ios::out);
        fstr << second << endl;
        fstr.close();
        fstr.open("third.txt", ios::out);
        fstr << third << endl;
        fstr.close();
        fstr.open("total.txt", ios::out);
        fstr << total << endl;
        fstr.close();

        /*
        fstr.open("1household.txt", ios::out);
        fstr << household << endl;
        fstr.close();
        fstr.open("2k12school.txt", ios::out);
        fstr << k12school << endl;
        fstr.close();
        fstr.open("3college.txt", ios::out);
        fstr << college << endl;
        fstr.close();
        fstr.open("4workplace.txt", ios::out);
        fstr << workplace << endl;
        fstr.close();
        fstr.open("5primary.txt", ios::out);
        fstr << primary << endl;
        fstr.close();
        fstr.open("6secondary.txt", ios::out);
        fstr << secondary << endl;
        fstr.close();
        fstr.open("7cluster.txt", ios::out);
        fstr << cluster << endl;
        fstr.close();
        */
}

void SimRunner::Run() { Run(m_config.get<unsigned int>("run.num_days")); }

} // namespace stride
