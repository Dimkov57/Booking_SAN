using DotNetEnv;
using BookingApi.Services;

Env.Load("../.env");   // підвантажує той самий .env що й Python

var builder = WebApplication.CreateBuilder(args);

// ── Services ──────────────────────────────────────────────────────────────────
builder.Services.AddSingleton<IDbConnectionFactory, NpgsqlConnectionFactory>();
builder.Services.AddScoped<UserService>();
builder.Services.AddScoped<BookingService>();

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// CORS — щоб Streamlit міг робити запити локально
builder.Services.AddCors(opt =>
    opt.AddDefaultPolicy(p =>
        p.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader()));

var app = builder.Build();

app.UseCors();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(); // http://localhost:5000/swagger
}

app.MapControllers();
app.Run();
