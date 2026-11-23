package ru.lab.core.interval;

public record Interval(double lower, double upper) {
    public Interval {
        if (!Double.isFinite(lower) || !Double.isFinite(upper) || lower > upper) {
            throw new IllegalArgumentException("interval bounds must be finite and ordered");
        }
    }
}
