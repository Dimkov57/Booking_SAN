using System.Data;
using Npgsql;

namespace BookingApi.Services;

public interface IDbConnectionFactory
{
    IDbConnection Create();
}

public class NpgsqlConnectionFactory : IDbConnectionFactory
{
    private readonly string _connStr;

    public NpgsqlConnectionFactory()
    {
        var host     = Environment.GetEnvironmentVariable("DB_HOST")     ?? "localhost";
        var port     = Environment.GetEnvironmentVariable("DB_PORT")     ?? "5432";
        var dbName   = Environment.GetEnvironmentVariable("DB_NAME")     ?? "booking_san";
        var user     = Environment.GetEnvironmentVariable("DB_USER")     ?? "postgres";
        var password = Environment.GetEnvironmentVariable("DB_PASSWORD") ?? "";

        _connStr = $"Host={host};Port={port};Database={dbName};Username={user};Password={password}";
    }

    public IDbConnection Create() => new NpgsqlConnection(_connStr);
}
