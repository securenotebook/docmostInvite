import psycopg2
import csv
import uuid
import os
from datetime import datetime

# Load environment variables
DB_HOST = os.getenv("DB_HOST", "docmost-db-1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "docmost")
DB_USER = os.getenv("DB_USER", "docmost")
DB_PASSWORD = os.getenv("DB_PASSWORD", "STRONG_DB_PASSWORD")  # Update as needed

# CSV file path
CSV_FILE = "invites.csv"

def get_connection():
    """Connect to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def get_workspace_id(workspace_name):
    """Find the workspace ID based on workspace name."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM workspaces WHERE name = %s;", (workspace_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print(f"Error: Workspace '{workspace_name}' not found.")
            return None
    except Exception as e:
        print(f"Error fetching workspace ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_user_id(user_email):
    """Find the user ID based on user email."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM users WHERE email = %s;", (user_email,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print(f"Error: User with email '{user_email}' not found.")
            return None
    except Exception as e:
        print(f"Error fetching user ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def create_invite(email, role, workspace_name, inviter_email):
    """Insert a new invite into the workspace_invitations table."""

    # Get the required IDs dynamically
    workspace_id = get_workspace_id(workspace_name)
    invited_by_id = get_user_id(inviter_email)

    if not workspace_id or not invited_by_id:
        print(f"Skipping {email}: Workspace or inviter ID not found.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    invitation_id = str(uuid.uuid4())  # Generate unique UUID
    token = uuid.uuid4().hex[:16]  # Generate a 16-character token
    created_at = updated_at = datetime.utcnow()

    try:
        cursor.execute(
            """
            INSERT INTO workspace_invitations (id, email, role, token, group_ids, invited_by_id, workspace_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, ARRAY[]::uuid[], %s, %s, %s, %s)
            """,
            (invitation_id, email, role, token, invited_by_id, workspace_id, created_at, updated_at),
        )
        conn.commit()
        print(f"Created invite for {email} in workspace '{workspace_name}' (Inviter: {inviter_email}).")
    except Exception as e:
        print(f"Error inserting {email}: {e}")
    finally:
        cursor.close()
        conn.close()

def bulk_create_invites():
    """Reads a CSV file and creates invites for each user."""
    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                email = row["email"].strip()
                role = row["role"].strip().lower()
                workspace_name = row["workspace_name"].strip()
                inviter_email = row["inviter_email"].strip()

                if role not in ["member", "admin"]:
                    print(f"Skipping {email}: Invalid role '{role}'")
                    continue

                create_invite(email, role, workspace_name, inviter_email)

        print("Bulk invite creation complete.")
    except FileNotFoundError:
        print(f"Error: File '{CSV_FILE}' not found.")

if __name__ == "__main__":
    bulk_create_invites()
