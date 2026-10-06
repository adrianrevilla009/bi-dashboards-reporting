package lab;

import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.util.HashMap;
import net.sf.jasperreports.engine.JasperCompileManager;
import net.sf.jasperreports.engine.JasperExportManager;
import net.sf.jasperreports.engine.JasperFillManager;
import net.sf.jasperreports.engine.JasperPrint;

/** Fills orders.jrxml from an in-memory SQLite database seeded with seed.sql and writes target/orders.pdf. */
public class RenderReport {
    public static void main(String[] args) throws Exception {
        try (Connection c = DriverManager.getConnection("jdbc:sqlite::memory:")) {
            try (Statement s = c.createStatement()) {
                for (String stmt : Files.readString(Path.of("seed.sql")).split(";\\s*\\n")) {
                    if (!stmt.isBlank()) s.execute(stmt);
                }
            }
            var report = JasperCompileManager.compileReport("orders.jrxml");
            JasperPrint print = JasperFillManager.fillReport(report, new HashMap<>(), c);
            Files.createDirectories(Path.of("target"));
            JasperExportManager.exportReportToPdfFile(print, "target/orders.pdf");
            System.out.println("wrote target/orders.pdf, pages=" + print.getPages().size());
        }
    }
}
