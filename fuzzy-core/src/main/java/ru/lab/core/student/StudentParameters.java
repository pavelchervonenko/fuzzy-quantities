package ru.lab.core.student;

public record StudentParameters(double center, double scale, int degreesOfFreedom) {
    public StudentParameters {
        if (!Double.isFinite(center)) {
            throw new IllegalArgumentException("center must be finite");
        }
        if (!Double.isFinite(scale) || scale <= 0.0) {
            throw new IllegalArgumentException("scale must be finite and greater than zero");
        }
        if (degreesOfFreedom <= 0) {
            throw new IllegalArgumentException("degreesOfFreedom must be greater than zero");
        }
    }
}
