package ru.lab.core.student;

import java.util.stream.Stream;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class StudentParametersTest {
    @ParameterizedTest
    @MethodSource("validParameters")
    void acceptsFiniteParametersIncludingRepresentableBoundaries(
            double center, double scale, int degreesOfFreedom) {
        var parameters = new StudentParameters(center, scale, degreesOfFreedom);

        assertEquals(center, parameters.center());
        assertEquals(scale, parameters.scale());
        assertEquals(degreesOfFreedom, parameters.degreesOfFreedom());
    }

    static Stream<Arguments> validParameters() {
        return Stream.of(
                Arguments.of(10.0, 2.0, 3),
                Arguments.of(0.0, 1.0, 1),
                Arguments.of(-0.0, Double.MIN_VALUE, 101),
                Arguments.of(-25.0, 0.25, 1_000),
                Arguments.of(Double.MAX_VALUE, Double.MAX_VALUE, Integer.MAX_VALUE),
                Arguments.of(-Double.MAX_VALUE, Double.MIN_NORMAL, 2));
    }

    @ParameterizedTest
    @MethodSource("nonFiniteValues")
    void rejectsNonFiniteCenter(double center) {
        var error = assertThrows(IllegalArgumentException.class,
                () -> new StudentParameters(center, 2.0, 3));
        assertEquals("center must be finite", error.getMessage());
    }

    @ParameterizedTest
    @MethodSource("invalidScales")
    void rejectsNonFiniteOrNonPositiveScale(double scale) {
        var error = assertThrows(IllegalArgumentException.class,
                () -> new StudentParameters(10.0, scale, 3));
        assertEquals("scale must be finite and greater than zero", error.getMessage());
    }

    static Stream<Double> nonFiniteValues() {
        return Stream.of(Double.NaN, Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY);
    }

    static Stream<Double> invalidScales() {
        return Stream.concat(nonFiniteValues(), Stream.of(0.0, -0.0, -1.0, -Double.MIN_VALUE));
    }

    @ParameterizedTest
    @ValueSource(ints = {0, -1, Integer.MIN_VALUE})
    void rejectsNonPositiveDegreesOfFreedom(int degreesOfFreedom) {
        var error = assertThrows(IllegalArgumentException.class,
                () -> new StudentParameters(10.0, 2.0, degreesOfFreedom));
        assertEquals("degreesOfFreedom must be greater than zero", error.getMessage());
    }
}
