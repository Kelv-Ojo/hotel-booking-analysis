// Create a text parameter CsvPath pointing to reports/excel_source.csv.
// New blank Power Query -> Advanced Editor. Name the query MonthlyImport.
// This companion script is not embedded in Hotel Reporting.xlsx.
let
    Source = Csv.Document(File.Contents(CsvPath), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {
        {"year", Int64.Type}, {"year_month", type text}, {"hotel", type text},
        {"distribution_channel", type text}, {"bookings", Int64.Type},
        {"canceled", Int64.Type}, {"checked_out", Int64.Type}, {"no_shows", Int64.Type}
    }),
    Check = Table.SelectRows(Typed, each [bookings] < 0 or [canceled] < 0 or [canceled] > [bookings]),
    Result = if Table.RowCount(Check) > 0 then error "Invalid booking or cancellation counts" else Typed
in
    Result
