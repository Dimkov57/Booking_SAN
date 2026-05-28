using Dapper;
using BookingApi.Models;

namespace BookingApi.Services;

public class BookingService(IDbConnectionFactory db)
{
    // Відповідає db.get_all_bookings()
    public IEnumerable<BookingDto> GetAll()
    {
        using var conn = db.Create();
        return conn.Query<BookingDto>("""
            SELECT b.booking_id AS Id,
                   u.first_name || ' ' || u.last_name AS Name,
                   b.student_id AS StudentId,
                   u.email      AS Email,
                   f.name       AS Faculty,
                   b.purpose    AS Purpose,
                   b.room_id    AS Room,
                   TO_CHAR(b.booking_date, 'YYYY-MM-DD')    AS Date,
                   ts.label     AS Slot,
                   TO_CHAR(b.booked_at, 'YYYY-MM-DD HH24:MI') AS BookedAt
            FROM bookings b
            JOIN users      u  ON u.student_id  = b.student_id
            JOIN faculties  f  ON f.faculty_id  = u.faculty_id
            JOIN time_slots ts ON ts.slot_id    = b.slot_id
            WHERE b.cancelled_at IS NULL
            ORDER BY b.booking_date, ts.start_time
            """);
    }

    // Відповідає db.add_booking()
    public bool Add(AddBookingRequest r)
    {
        try
        {
            using var conn = db.Create();
            // Нормалізуємо роздільник слоту: "08:00-09:30" або "08:00–09:30" → шукаємо обидва
            conn.Execute("""
                INSERT INTO bookings
                    (booking_id, student_id, room_id, slot_id,
                     booking_date, purpose, booked_at)
                SELECT @Id, @StudentId, @Room, slot_id,
                       @Date::date, @Purpose, @BookedAt::timestamptz
                FROM time_slots
                WHERE replace(label, '–', '-') = replace(@Slot, '–', '-')
                """, r);
            return true;
        }
        catch (Npgsql.PostgresException ex) when (ex.SqlState == "23505")
        {
            return false;
        }
    }

    // Відповідає db.cancel_booking()
    public void Cancel(string bookingId)
    {
        using var conn = db.Create();
        conn.Execute(
            "UPDATE bookings SET cancelled_at = NOW() WHERE booking_id = @Id",
            new { Id = bookingId });
    }
}
