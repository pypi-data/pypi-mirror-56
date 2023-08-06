//    Copyright 2019 Jij Inc.

//    Licensed under the Apache License, Version 2.0 (the "License");
//    you may not use this file except in compliance with the License.
//    You may obtain a copy of the License at

//        http://www.apache.org/licenses/LICENSE-2.0

//    Unless required by applicable law or agreed to in writing, software
//    distributed under the License is distributed on an "AS IS" BASIS,
//    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//    See the License for the specific language governing permissions and
//    limitations under the License.

#ifndef OPENJIJ_UTILITY_SCHEDULE_LIST_HPP__
#define OPENJIJ_UTILITY_SCHEDULE_LIST_HPP__

#include <cstddef>
#include <cmath>
#include <vector>

#include <system/system.hpp>

namespace openjij {
    namespace utility {

        /**
         * @brief updater parameter for monte carlo simulation
         *
         * @tparam SystemType system type
         */
        template<typename SystemType>
        struct UpdaterParameter;

        /**
         * @brief updater parameter for classical ising system
         */
        template<>
        struct UpdaterParameter<system::classical_system> {
            UpdaterParameter() = default;
            UpdaterParameter(double beta) : beta{beta} {}

            /**
             * @brief inverse temperature
             */
            double beta;
        };

        /**
         * @brief updater paramter for transverse ising model
         */
        template<>
        struct UpdaterParameter<system::transverse_field_system> {
            UpdaterParameter() = default;
            UpdaterParameter(double beta, double s) : beta{beta}, s{s} {}

            /**
             * @brief inverse temperature
             */
            double beta;

            /**
             * @brief annealing schedule (from 0 (only transverse field) to 1 (only classical Hamiltonian))
             */
            double s;
        };

        //TODO: add UpdaterParameter here if needed.

        /**
         * @brief ClassicalUpdaterParameter alias
         */
        using ClassicalUpdaterParameter = UpdaterParameter<system::classical_system>;

        /**
         * @brief TransverseFieldUpdaterParameter alias
         */
        using TransverseFieldUpdaterParameter = UpdaterParameter<system::transverse_field_system>;

        /**
         * @brief schedule struct
         *
         * @tparam SystemType system type
         */
        template<typename SystemType>
        struct Schedule {
            Schedule() = default;
            std::size_t one_mc_step;
            UpdaterParameter<SystemType> updater_parameter;
        };

        /**
         * @brief schedule list alias
         *
         * @tparam SystemType system type
         */
        template<typename SystemType>
        using ScheduleList = std::vector<Schedule<SystemType>>;

        /**
         * @brief ClassicalScheduleList alias
         */
        using ClassicalScheduleList = ScheduleList<system::classical_system>;

        /**
         * @brief TransverseFieldScheduleList alias
         */
        using TransverseFieldScheduleList = ScheduleList<system::transverse_field_system>;

        /**
         * @brief helper function for making classical schedule list with geometric series of inverse temperatures.
         *
         * @param beta_min initial (minimal) value of beta 
         * @param beta_max final (maximal) value of beta
         * @param one_mc_step number of mc step for each temperature
         * @param num_call_updater number of updater calls
         *
         * @return generated list
         */
        ClassicalScheduleList make_classical_schedule_list(double beta_min, double beta_max, std::size_t one_mc_step, std::size_t num_call_updater) {
            double r_beta = std::pow(beta_max/beta_min, 1.0/static_cast<double>(num_call_updater - 1));
            double beta = beta_min;

            auto schedule_list = ClassicalScheduleList(num_call_updater);
            for (auto& schedule : schedule_list) {
                schedule.one_mc_step = one_mc_step;
                schedule.updater_parameter = ClassicalUpdaterParameter(beta);
                beta *= r_beta;
            }

            return schedule_list;
        }

        /**
         * @brief helper function for making transverse field system schedule list with arithmetic sequence of annealing schedule (s)
         *
         * @param beta inverse temperature
         * @param one_mc_step number of mc step for each temperature
         * @param num_call_updater number of updater calls
         *
         * @return 
         */
        TransverseFieldScheduleList make_transverse_field_schedule_list(double beta, std::size_t one_mc_step, std::size_t num_call_updater) {
            double ds = 1.0/static_cast<double>(num_call_updater - 1);
            double s = 0;

            auto schedule_list = TransverseFieldScheduleList(num_call_updater);
            for (auto& schedule : schedule_list) {
                schedule.one_mc_step = one_mc_step;
                schedule.updater_parameter = TransverseFieldUpdaterParameter(beta, s);
                s += ds;
            }

            return schedule_list;
        }

    } // namespace utility
} // namespace openjij

#endif
