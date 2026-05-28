using Microsoft.AspNetCore.Mvc;
using BookingApi.Models;
using BookingApi.Services;

namespace BookingApi.Controllers;

[ApiController]
[Route("api/users")]
public class UsersController(UserService users) : ControllerBase
{
    // GET /api/users
    [HttpGet]
    public IActionResult GetAll() =>
        Ok(users.GetAll());

    // POST /api/users
    [HttpPost]
    public IActionResult Create([FromBody] CreateUserRequest request)
    {
        var ok = users.Create(request);
        return ok ? Created() : Conflict(new { error = "Student ID or email already exists." });
    }

    // PUT /api/users/{studentId}
    [HttpPut("{studentId}")]
    public IActionResult Update(string studentId, [FromBody] UpdateUserRequest request)
    {
        users.Update(studentId, request);
        return NoContent();
    }

    // PATCH /api/users/{studentId}/password
    [HttpPatch("{studentId}/password")]
    public IActionResult UpdatePassword(string studentId, [FromBody] UpdatePasswordRequest request)
    {
        users.UpdatePassword(studentId, request);
        return NoContent();
    }
}
