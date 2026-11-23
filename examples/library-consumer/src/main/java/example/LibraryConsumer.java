package example;

import java.util.Locale;
import ru.lab.core.interval.Interval;
import ru.lab.core.student.BoundedStudentFuzzyNumber;
import ru.lab.core.student.StudentParameters;

/** Uses the public Java API through built JARs, without source directories or JavaFX. */
public final class LibraryConsumer {
    private LibraryConsumer() {
    }

    public static void main(String[] args) {
        var parameters = new StudentParameters(10.0, 2.0, 5);
        System.out.printf(Locale.ROOT, "StudentParameters: center=%.1f, scale=%.1f, degreesOfFreedom=%d%n",
                parameters.center(), parameters.scale(), parameters.degreesOfFreedom());

        var number = new BoundedStudentFuzzyNumber(parameters, 0.001);
        Interval support = number.support();
        Interval peak = number.alphaCut(1.0);
        System.out.printf(Locale.ROOT, "epsilon=%.3f, membership(10)=%.1f%n", number.epsilon(), number.membership(10.0));
        System.out.printf(Locale.ROOT, "alpha=0: [%.4f, %.4f]%n", support.lower(), support.upper());
        System.out.printf(Locale.ROOT, "alpha=1: [%.4f, %.4f]%n", peak.lower(), peak.upper());
    }
}
