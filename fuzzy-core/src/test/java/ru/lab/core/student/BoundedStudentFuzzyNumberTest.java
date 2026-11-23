package ru.lab.core.student;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import ru.lab.core.interval.Interval;
import ru.lab.core.model.FuzzyNumber;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BoundedStudentFuzzyNumberTest {
    private static final double TOLERANCE = 2e-12;
    private static final StudentParameters PARAMETERS = new StudentParameters(2.0, 1.0, 1);

    @Test
    void computesMembershipAndCutsForAnExactlyKnownShape() {
        FuzzyNumber number = new BoundedStudentFuzzyNumber(PARAMETERS, 0.5);

        assertEquals(new Interval(1.0, 3.0), number.alphaCut(0.0));
        assertEquals(number.alphaCut(0.0), number.support());
        assertEquals(new Interval(2.0, 2.0), number.alphaCut(1.0));
        assertEquals(1.0, number.membership(2.0));
        assertEquals(0.6, number.membership(1.5), TOLERANCE);
        assertEquals(0.6, number.membership(2.5), TOLERANCE);
        assertEquals(0.0, number.membership(1.0));
        assertEquals(0.0, number.membership(3.0));
        assertEquals(0.0, number.membership(-Double.MAX_VALUE));
        assertEquals(0.0, number.membership(Double.MAX_VALUE));

        double halfCutRadius = 1.0 / Math.sqrt(3.0);
        assertEquals(2.0 - halfCutRadius, number.alphaCut(0.5).lower(), TOLERANCE);
        assertEquals(2.0 + halfCutRadius, number.alphaCut(0.5).upper(), TOLERANCE);
    }

    @ParameterizedTest
    @ValueSource(ints = {1, 5, 10, Integer.MAX_VALUE})
    void cutsAreNestedAndMembershipOnTheirBoundsMatchesAlpha(int degreesOfFreedom) {
        var number = new BoundedStudentFuzzyNumber(new StudentParameters(10.0, 2.0, degreesOfFreedom), 0.001);
        Interval previous = number.support();
        if (degreesOfFreedom == 5) {
            double expectedRadius = 2.0 * Math.sqrt(45.0);
            assertEquals(10.0 - expectedRadius, previous.lower(), TOLERANCE);
            assertEquals(10.0 + expectedRadius, previous.upper(), TOLERANCE);
        }

        for (int step = 0; step <= 100; step++) {
            double alpha = step / 100.0;
            Interval cut = number.alphaCut(alpha);
            assertTrue(previous.lower() <= cut.lower() && cut.upper() <= previous.upper(),
                    "cuts must be nested at alpha=" + alpha);
            assertEquals(alpha, number.membership(cut.lower()), TOLERANCE);
            assertEquals(alpha, number.membership(cut.upper()), TOLERANCE);
            previous = cut;
        }
    }

    @Test
    void preservesTheCutNearOneWhenTheThresholdRoundsToOne() {
        var number = new BoundedStudentFuzzyNumber(new StudentParameters(0.0, 1.0, 1), Math.nextDown(1.0));
        Interval cut = number.alphaCut(0.75);

        assertTrue(cut.upper() > 0.0);
        assertEquals(0.75, number.membership(cut.upper()), TOLERANCE);
        assertEquals(0.0, number.membership(number.support().upper()), TOLERANCE);
    }

    @Test
    void handlesTinyEpsilonWithoutOverflowInTheIntermediateSquare() {
        double scale = 1e-100;
        var number = new BoundedStudentFuzzyNumber(new StudentParameters(0.0, scale, 1), Double.MIN_VALUE);
        double expectedRadius = scale / Math.sqrt(Double.MIN_VALUE);

        assertEquals(expectedRadius, number.support().upper(), expectedRadius * TOLERANCE);
        assertEquals(3.0 * Double.MIN_VALUE, number.membership(expectedRadius / 2.0));
    }

    @Test
    void computesMembershipAtARoundedSupportEndpointFromTheActualPoint() {
        double center = 1e16;
        var number = new BoundedStudentFuzzyNumber(new StudentParameters(center, 2.5, 1), 0.5);

        assertEquals(center + 2.0, number.support().upper());
        assertEquals(9.0 / 41.0, number.membership(center + 2.0), TOLERANCE);
    }

    @ParameterizedTest
    @ValueSource(doubles = {Double.NaN, Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY, -0.1, -0.0, 0.0, 1.0, 1.1})
    void rejectsInvalidEpsilon(double epsilon) {
        assertThrows(IllegalArgumentException.class, () -> new BoundedStudentFuzzyNumber(PARAMETERS, epsilon));
    }

    @Test
    void rejectsMissingParameters() {
        assertThrows(NullPointerException.class, () -> new BoundedStudentFuzzyNumber(null, 0.5));
    }

    @ParameterizedTest
    @ValueSource(doubles = {Double.NaN, Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY, -Double.MIN_VALUE, 1.01})
    void rejectsInvalidAlpha(double alpha) {
        var number = new BoundedStudentFuzzyNumber(PARAMETERS, 0.5);
        assertThrows(IllegalArgumentException.class, () -> number.alphaCut(alpha));
    }

    @ParameterizedTest
    @ValueSource(doubles = {Double.NaN, Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY})
    void rejectsNonFinitePoints(double x) {
        var number = new BoundedStudentFuzzyNumber(PARAMETERS, 0.5);
        assertThrows(IllegalArgumentException.class, () -> number.membership(x));
    }

    @Test
    void rejectsOverflowInSupportRadiusOrBounds() {
        assertThrows(ArithmeticException.class, () -> new BoundedStudentFuzzyNumber(
                new StudentParameters(0.0, Double.MAX_VALUE, 1), 0.25));
        assertThrows(ArithmeticException.class, () -> new BoundedStudentFuzzyNumber(
                new StudentParameters(Double.MAX_VALUE, Double.MAX_VALUE / 2.0, 1), 0.5));
    }
}
