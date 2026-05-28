using Microsoft.AspNetCore.Mvc;
using BookingApi.Models;
using BookingApi.Services;

namespace BookingApi.Controllers;

[ApiController]
[Route("api/bookings")]
public class BookingsController(BookingService bookings) : ControllerBase
{
    // GET /api/bookings
    [HttpGet]
    public IActionResult GetAll() =>
        Ok(bookings.GetAll());

    // POST /api/bookings
    [HttpPost]
    public IActionResult Add([FromBody] AddBookingRequest request)
    {
        var ok = bookings.Add(request);
        return ok ? Created() : Conflict(new { error = "Booking ID already exists." });
    }

    // DELETE /api/bookings/{bookingId}
    [HttpDelete("{bookingId}")]
    public IActionResult Cancel(string bookingId)
    {
        bookings.Cancel(bookingId);
        return NoContent();
    }
}
