namespace BookingApi.Models;

// ── Users ─────────────────────────────────────────────────────────────────────

public record UserDto(
    string StudentId,
    string FirstName,
    string LastName,
    string Name,          // first_name + ' ' + last_name
    string Email,
    string Faculty,
    string Password,      // SHA-256 hex
    string Joined         // "YYYY-MM-DD"
);

public record CreateUserRequest(
    string StudentId,
    string FirstName,
    string LastName,
    string Email,
    string Faculty,
    string PasswordHash,
    string Joined
);

public record UpdateUserRequest(
    string FirstName,
    string LastName,
    string Email,
    string Faculty
);

public record UpdatePasswordRequest(
    string PasswordHash
);

// ── Bookings ──────────────────────────────────────────────────────────────────

public record BookingDto(
    string Id,
    string Name,          // student full name
    string StudentId,
    string Email,
    string Faculty,
    string Purpose,
    string Room,
    string Date,          // "YYYY-MM-DD"
    string Slot,          // "08:00-09:30"
    string BookedAt       // "YYYY-MM-DD HH:MM"
);

public record AddBookingRequest(
    string Id,
    string Name,
    string StudentId,
    string Email,
    string Faculty,
    string Purpose,
    string Room,
    string Date,
    string Slot,
    string BookedAt
);
