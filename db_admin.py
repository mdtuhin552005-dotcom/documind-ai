"""
Database Admin Script - DocuMind AI
Run: .venv\\Scripts\\python.exe db_admin.py
"""
import asyncio
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
from pathlib import Path

# Project root যোগ করো
sys.path.insert(0, str(Path(__file__).parent))
from app.database import DocumentDatabase

DB_PATH = Path("data/documind.db")
db = DocumentDatabase(DB_PATH)


async def show_tables():
    """সব table এবং তাদের row count দেখাও"""
    import aiosqlite
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [r[0] for r in await cursor.fetchall()]
        print("\n📋 DATABASE TABLES")
        print("=" * 40)
        for t in tables:
            c = await conn.execute(f"SELECT COUNT(*) FROM {t}")
            count = (await c.fetchone())[0]
            print(f"  {t:<30} {count:>5} rows")
        print()


async def show_users():
    """সব user দেখাও"""
    import aiosqlite
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute(
            "SELECT id, email, full_name, created_at FROM users ORDER BY created_at"
        )
        rows = await cursor.fetchall()
        print("\n👤 USERS")
        print("=" * 70)
        if not rows:
            print("  কোনো user নেই।")
        for r in rows:
            print(f"  ID: {r['id'][:8]}...  Email: {r['email']:<30}  Name: {r['full_name']}")
        print()


async def show_documents():
    """সব document দেখাও"""
    import aiosqlite
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute(
            "SELECT id, filename, title, page_count, created_at FROM documents ORDER BY created_at DESC"
        )
        rows = await cursor.fetchall()
        print("\n📄 DOCUMENTS")
        print("=" * 70)
        if not rows:
            print("  কোনো document নেই।")
        for r in rows:
            print(f"  [{r['id'][:6]}] {r['filename']:<30} Pages: {r['page_count']}  Date: {r['created_at'][:10]}")
        print()


async def show_conversations():
    """সব conversation দেখাও"""
    import aiosqlite
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute(
            "SELECT id, title, updated_at FROM conversations ORDER BY updated_at DESC LIMIT 20"
        )
        rows = await cursor.fetchall()
        print("\n💬 CONVERSATIONS (সর্বশেষ ২০টি)")
        print("=" * 70)
        if not rows:
            print("  কোনো conversation নেই।")
        for r in rows:
            print(f"  [{r['id'][:6]}] {r['title'][:50]:<50}  {r['updated_at'][:10]}")
        print()


async def delete_user(email: str):
    """একজন user delete করো (email দিয়ে)"""
    import aiosqlite
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("SELECT id, email FROM users WHERE lower(email) = lower(?)", (email,))
        user = await cursor.fetchone()
        if not user:
            print(f"❌ User পাওয়া যায়নি: {email}")
            return
        confirm = input(f"⚠️  '{user[1]}' delete করবে? (yes/no): ")
        if confirm.lower() == "yes":
            await conn.execute("DELETE FROM sessions WHERE user_id = ?", (user[0],))
            await conn.execute("DELETE FROM users WHERE id = ?", (user[0],))
            await conn.commit()
            print(f"✅ User deleted: {email}")
        else:
            print("বাতিল।")


async def clear_all_sessions():
    """সব session মুছে দাও (সবাইকে logout করো)"""
    import aiosqlite
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("DELETE FROM sessions")
        await conn.commit()
        print(f"✅ {cursor.rowcount} sessions deleted। সবাই logout হয়ে গেছে।")


async def raw_sql(query: str):
    """Custom SQL চালাও"""
    import aiosqlite
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        try:
            cursor = await conn.execute(query)
            if query.strip().upper().startswith("SELECT"):
                rows = await cursor.fetchall()
                if rows:
                    keys = rows[0].keys()
                    print("  " + " | ".join(f"{k:<15}" for k in keys))
                    print("  " + "-" * (17 * len(keys)))
                    for r in rows:
                        print("  " + " | ".join(f"{str(r[k]):<15}" for k in keys))
                else:
                    print("  কোনো result নেই।")
            else:
                await conn.commit()
                print(f"✅ Done। Affected rows: {cursor.rowcount}")
        except Exception as e:
            print(f"❌ Error: {e}")


async def main():
    await db.initialize()

    MENU = """
╔══════════════════════════════════════╗
║   DocuMind DB Admin Panel            ║
╠══════════════════════════════════════╣
║  1. সব table দেখাও                  ║
║  2. সব user দেখাও                   ║
║  3. সব document দেখাও               ║
║  4. সব conversation দেখাও           ║
║  5. User delete করো                  ║
║  6. সব session clear করো            ║
║  7. Custom SQL চালাও                 ║
║  0. বের হও                          ║
╚══════════════════════════════════════╝
"""
    while True:
        print(MENU)
        choice = input("➤ Select: ").strip()
        if choice == "1":
            await show_tables()
        elif choice == "2":
            await show_users()
        elif choice == "3":
            await show_documents()
        elif choice == "4":
            await show_conversations()
        elif choice == "5":
            email = input("Delete করার User এর Email: ").strip()
            await delete_user(email)
        elif choice == "6":
            await clear_all_sessions()
        elif choice == "7":
            query = input("SQL Query: ").strip()
            await raw_sql(query)
        elif choice == "0":
            print("👋 বের হচ্ছি...")
            break
        else:
            print("❌ ভুল choice। আবার দাও।")


if __name__ == "__main__":
    asyncio.run(main())
