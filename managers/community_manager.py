from managers.base_manager import BaseManager
from services.database import DISCOUNT


class CommunityManager(BaseManager):
    def get_community_discount(self, user_id):
        """Return the discount value for the user's community, if any."""
        cursor = self._db.connection.cursor()
        cursor.execute("""
            SELECT c.discount FROM users u 
            JOIN communities c ON u.community_id = c.id 
            WHERE u.id = ?
        """, (user_id,))
        row = cursor.fetchone()
        return row[DISCOUNT] if row else 0.0

    def get_communities(self):
        cursor = self._db.connection.cursor()
        cursor.execute("SELECT * FROM communities")
        return cursor.fetchall()

    def show_communities(self):
        print("Available communities:")
        communities = self.get_communities()
        for comm in communities:
            print(f"ID: {comm['id']}, Name: {comm['name']}")

    def get_users_with_community_discount(self):
        cursor = self._db.connection.cursor()
        cursor.execute("SELECT id, username, community_id FROM users WHERE community_id IS NOT NULL")
        return cursor.fetchall()

    def show_users_with_community_discount(self):
        customers = self.get_users_with_community_discount()
        if not customers:
            print("No customers with community discount found.")
            return
        for cust in customers:
            print(f"ID: {cust['id']}, Username: {cust['username']}, Community ID: {cust['community_id']}")

    def cancel_community_discount(self, user_id):
        cursor = self._db.connection.cursor()
        cursor.execute("UPDATE users SET community_id = NULL WHERE id = ?", (user_id,))
        self._db.connection.commit()
        print("Community discount cancelled for the customer.")