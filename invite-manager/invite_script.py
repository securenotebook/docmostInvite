import psycopg2
import os

# Database connection details
DB_HOST = os.getenv("DB_HOST", "docmost-db-1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "docmost")
DB_USER = os.getenv("POSTGRES_USER", "docmost")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "your_password")  # Update as needed

# Docmost instance base URL from environment variable
DOCMOST_URL = os.getenv("DOCMOST_URL", "http://localhost:5010")

def get_connection():
    """Connect to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def list_invites():
    """Fetch workspace invitations and print invite URLs."""
    query = "SELECT email, id, token FROM workspace_invitations"

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)

        invites = cursor.fetchall()
        if not invites:
            print("No invitations found.")

        else:
            print("\nWorkspace Invitations:")
            for invite in invites:
                email, invite_id, token = invite
                invite_url = f"{DOCMOST_URL}/invites/{invite_id}?token={token}"
                print(f"{email}: {invite_url}")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error fetching invites: {e}")

if __name__ == "__main__":
    list_invites()
