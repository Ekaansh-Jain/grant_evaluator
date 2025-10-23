"""Test MongoDB connection"""
import asyncio
import traceback
import database


async def main():
    try:
        print("Attempting to connect to MongoDB...")
        await database.connect_to_mongo()
        print("✅ Connected successfully!")

        eval_coll = database.evaluations_collection
        settings_coll = database.settings_collection

        print(f"Evaluations collection object: {eval_coll}")
        print(f"Settings collection object: {settings_coll}")

        # Try to count documents if the collection is available
        if eval_coll is not None:
            count = await eval_coll.count_documents({})
            print(f"Number of evaluations in database: {count}")
        else:
            print("Evaluations collection is not initialized.")

    except Exception as e:
        print("❌ Connection or query failed!")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
