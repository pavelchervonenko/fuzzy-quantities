package ru.lab.core.model;

import ru.lab.core.interval.Interval;

/** A fuzzy number with finite, nested closed alpha-cuts. */
public interface FuzzyNumber {
    /**
     * Returns the membership of a finite point in [0, 1].
     *
     * @throws IllegalArgumentException if the point is non-finite
     */
    double membership(double x);

    /**
     * Returns the cut at alpha. At alpha zero this is the closure of the positive support.
     *
     * @throws IllegalArgumentException if alpha is non-finite or outside [0, 1]
     */
    Interval alphaCut(double alpha);

    /** Returns the closed support, including its endpoints. */
    default Interval support() {
        return alphaCut(0.0);
    }
}
