package ru.lab.core.student;

import java.util.Objects;
import ru.lab.core.interval.Interval;
import ru.lab.core.model.FuzzyNumber;

public final class BoundedStudentFuzzyNumber implements FuzzyNumber {
    private final StudentParameters parameters;
    private final double epsilon;
    private final Interval support;

    public BoundedStudentFuzzyNumber(StudentParameters parameters, double epsilon) {
        this.parameters = Objects.requireNonNull(parameters, "parameters");
        if (!Double.isFinite(epsilon) || epsilon <= 0.0 || epsilon >= 1.0) {
            throw new IllegalArgumentException("epsilon must be finite and in (0, 1)");
        }
        this.epsilon = epsilon;
        this.support = calculateCut(0.0);
    }

    public StudentParameters parameters() {
        return parameters;
    }

    public double epsilon() {
        return epsilon;
    }

    @Override
    public double membership(double x) {
        if (!Double.isFinite(x)) {
            throw new IllegalArgumentException("x must be finite");
        }
        double center = parameters.center();
        if (x == center) {
            return 1.0;
        }
        if (x < support.lower() || x > support.upper()) {
            return 0.0;
        }

        double degrees = parameters.degreesOfFreedom();
        double z = ((x - center) / parameters.scale()) / Math.sqrt(degrees);
        double squared = z * z;
        // When z squared overflows, dropping the 1 in log(1 + z squared) has negligible error.
        double logBase = Double.isFinite(squared) ? Math.log1p(squared) : 2.0 * Math.log(Math.abs(z));
        double logMembership = -(degrees + 1.0) / 2.0 * logBase;
        // With epsilon close to one, work with 1 - raw membership to preserve the difference.
        double bounded = epsilon > 0.5
                ? 1.0 + Math.expm1(logMembership) / (1.0 - epsilon)
                : (Math.exp(logMembership) - epsilon) / (1.0 - epsilon);
        return Math.clamp(bounded, 0.0, 1.0);
    }

    @Override
    public Interval alphaCut(double alpha) {
        if (!Double.isFinite(alpha) || alpha < 0.0 || alpha > 1.0) {
            throw new IllegalArgumentException("alpha must be finite and in [0, 1]");
        }
        if (alpha == 0.0) {
            return support;
        }
        if (alpha == 1.0) {
            return new Interval(parameters.center(), parameters.center());
        }
        return calculateCut(alpha);
    }

    private Interval calculateCut(double alpha) {
        // Use the deficit 1 - q near one, and q itself near zero.
        double deficit = (1.0 - epsilon) * (1.0 - alpha);
        double logThreshold = deficit <= 0.5
                ? Math.log1p(-deficit)
                : Math.log(Math.fma(1.0 - epsilon, alpha, epsilon));

        double degrees = parameters.degreesOfFreedom();
        double exponent = -2.0 * logThreshold / (degrees + 1.0);
        // Factor exp(exponent) out of the square root to avoid overflow before taking the root.
        double radiusInScales = Math.exp(exponent / 2.0) * Math.sqrt(-degrees * Math.expm1(-exponent));
        double radius = parameters.scale() * radiusInScales;
        double lower = parameters.center() - radius;
        double upper = parameters.center() + radius;
        if (!Double.isFinite(lower) || !Double.isFinite(upper)) {
            throw new ArithmeticException("alpha-cut bounds cannot be represented as finite doubles");
        }
        return new Interval(lower, upper);
    }
}
