using Dapper;
using BookingApi.Models;

namespace BookingApi.Services;

public class UserService(IDbConnectionFactory db)
{
    // Відповідає db.get_all_users()
    public IEnumerable<UserDto> GetAll()
    {
        using var conn = db.Create();
        return conn.Query<UserDto>("""
            SELECT u.student_id  AS StudentId,
                   u.first_name  AS FirstName,
                   u.last_name   AS LastName,
                   u.first_name || ' ' || u.last_name AS Name,
                   u.email       AS Email,
                   f.name        AS Faculty,
                   u.password    AS Password,
                   TO_CHAR(u.joined, 'YYYY-MM-DD') AS Joined
            FROM users u
            JOIN faculties f ON f.faculty_id = u.faculty_id
            ORDER BY u.last_name, u.first_name
            """);
    }

    // Відповідає db.create_user()
    public bool Create(CreateUserRequest r)
    {
        try
        {
            using var conn = db.Create();
            conn.Execute("""
                INSERT INTO users (student_id, first_name, last_name, email,
                                   faculty_id, password, joined)
                VALUES (@StudentId, @FirstName, @LastName, @Email,
                        (SELECT faculty_id FROM faculties WHERE name = @Faculty),
                        @PasswordHash, @Joined::date)
                """, r);
            return true;
        }
        catch (Npgsql.PostgresException ex) when (ex.SqlState == "23505") // unique violation
        {
            return false;
        }
    }

    // Відповідає db.update_user()
    public void Update(string studentId, UpdateUserRequest r)
    {
        using var conn = db.Create();
        conn.Execute("""
            UPDATE users
               SET first_name = @FirstName,
                   last_name  = @LastName,
                   email      = @Email,
                   faculty_id = (SELECT faculty_id FROM faculties WHERE name = @Faculty)
             WHERE student_id = @StudentId
            """, new { r.FirstName, r.LastName, r.Email, r.Faculty, StudentId = studentId });
    }

    // Відповідає db.update_password()
    public void UpdatePassword(string studentId, UpdatePasswordRequest r)
    {
        using var conn = db.Create();
        conn.Execute(
            "UPDATE users SET password = @PasswordHash WHERE student_id = @StudentId",
            new { r.PasswordHash, StudentId = studentId });
    }
}
