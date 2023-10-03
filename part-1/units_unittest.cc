// Kevin Wortman
// kwortman@fullerton.edu
// @kevinwortman
// Partners: @mshafae
//
// Convert ml to US customary measurements
//

/* Do not edit below this line. */
/* Do not edit below this line. */
/* Do not edit below this line. */

#include <gtest/gtest.h>

#include <climits>
#include <cstdio>
#include <future>

#include "units_functions.h"

// Thanks to Paul Inventado
// https://github.com/google/googletest/issues/348#issuecomment-431714269
#define MAX_DURATION_MS 500
// Fail immediately.
// NOLINT(cppcoreguidelines-macro-usage)
#define ASSERT_DURATION_LE(millisecs, stmt)                                 \
  {                                                                         \
    std::promise<bool> completed;                                           \
    auto stmt_future = completed.get_future();                              \
    std::thread(                                                            \
        [&](std::promise<bool>& completed) {                                \
          stmt;                                                             \
          completed.set_value(true);                                        \
        },                                                                  \
        std::ref(completed))                                                \
        .detach();                                                          \
    if (stmt_future.wait_for(std::chrono::milliseconds(millisecs)) ==       \
        std::future_status::timeout)                                        \
      GTEST_FATAL_FAILURE_("\tExecution time greater than " #millisecs      \
                           " milliseconds.\n\tRevise algorithm for better " \
                           "performance and check for "                     \
                           "infinite loops.");                              \
  }

// Defer failure
// NOLINT(cppcoreguidelines-macro-usage)
#define EXPECT_DURATION_LE(millisecs, stmt)                                    \
  {                                                                            \
    std::promise<bool> completed;                                              \
    auto stmt_future = completed.get_future();                                 \
    std::thread(                                                               \
        [&](std::promise<bool>& completed) {                                   \
          stmt;                                                                \
          completed.set_value(true);                                           \
        },                                                                     \
        std::ref(completed))                                                   \
        .detach();                                                             \
    if (stmt_future.wait_for(std::chrono::milliseconds(millisecs)) ==          \
        std::future_status::timeout)                                           \
      GTEST_NONFATAL_FAILURE_("\tExecution time greater than " #millisecs      \
                              " milliseconds.\n\tRevise algorithm for better " \
                              "performance and check for "                     \
                              "infinite loops.");                              \
  }

#define FP_DELTA 0.001
namespace {

// Tests RectangleArea()

// Tests negative input.
TEST(UnitsTeaspoonTest, Negative) {
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-1.0144, MlToTsp(-5), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-0.0249544, MlToTsp(-0.123), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-0.680868, MlToTsp(-3.356), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-266.293, MlToTsp(-1312.56), FP_DELTA));
}

// Tests positive input.
TEST(UnitsTeaspoonTest, Positive) {
  EXPECT_DURATION_LE(MAX_DURATION_MS, EXPECT_NEAR(0, MlToTsp(0), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(1.0144, MlToTsp(5), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(0.0249544, MlToTsp(0.123), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(0.680868, MlToTsp(3.356), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(266.293, MlToTsp(1312.56), FP_DELTA));
}

// Tests negative input.
TEST(UnitsTablespoonTest, Negative) {
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-0.338135, MlToTbsp(-5), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-0.00831812, MlToTbsp(-0.123), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-0.226956, MlToTbsp(-3.356), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-88.7645, MlToTbsp(-1312.56), FP_DELTA));
}

// Tests positive input.
TEST(UnitsTablespoonTest, Positive) {
  EXPECT_DURATION_LE(MAX_DURATION_MS, EXPECT_NEAR(0, MlToTbsp(0), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(0.338135, MlToTbsp(5), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(0.00831812, MlToTbsp(0.123), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(0.226956, MlToTbsp(3.356), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(88.7645, MlToTbsp(1312.56), FP_DELTA));
}

// Tests negative input.
TEST(UnitsOunceTest, Negative) {
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-0.169067, MlToOz(-5), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-0.00415906, MlToOz(-0.123), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-0.113478, MlToOz(-3.356), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-44.3822, MlToOz(-1312.56), FP_DELTA));
}

// Tests positive input.
TEST(UnitsOunceTest, Positive) {
  EXPECT_DURATION_LE(MAX_DURATION_MS, EXPECT_NEAR(0, MlToOz(0), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(0.169067, MlToOz(5), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(0.00415906, MlToOz(0.123), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(0.113478, MlToOz(3.356), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(44.3822, MlToOz(1312.56), FP_DELTA));
}

// Tests negative input.
TEST(UnitsCupTest, Negative) {
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-0.0211334, MlToCup(-5), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-0.000519882, MlToCup(-0.123), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-0.0141848, MlToCup(-3.356), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(-5.54778, MlToCup(-1312.56), FP_DELTA));
}

// Tests positive input.
TEST(UnitsCupTest, Positive) {
  EXPECT_DURATION_LE(MAX_DURATION_MS, EXPECT_NEAR(0, MlToCup(0), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(0.0211334, MlToCup(5), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(0.000519882, MlToCup(0.123), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(0.0141848, MlToCup(3.356), FP_DELTA));
  EXPECT_DURATION_LE(MAX_DURATION_MS,
                     EXPECT_NEAR(5.54778, MlToCup(1312.56), FP_DELTA));
}

}  // namespace
