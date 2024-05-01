from api.config import supabase

class SupabaseDashboard:

    def get(table_name: str, query: str):
        response_from_supabase = supabase.table(table_name)\
            .select(query)\
            .execute()
        return response_from_supabase
        
    def get_by_condition(table_name: str, query: str, column: str, value: any):
        response_from_supabase = supabase.table(table_name)\
            .select(query)\
            .eq(column=column, value=value)\
            .execute()
        return response_from_supabase
    
    def insert(table_name: str, data: dict):
        response_from_supabase = supabase.table(table_name)\
            .insert(data)\
            .execute()
        return response_from_supabase
    
    def update(table_name: str, data: dict, column: str, value: any):
        response_from_supabase = supabase.table(table_name)\
            .update(data)\
            .eq(column=column, value=value)\
            .execute()
        return response_from_supabase
    
    def upsert(table_name: str, data: dict):
        response_from_supabase = supabase.table(table_name)\
            .upsert(data)\
            .execute()
        return response_from_supabase
    
    def delete(table_name: str, column: str, value: any):
        response_from_supabase = supabase.table(table_name)\
            .delete()\
            .eq(column=column, value=value)\
            .execute()
        return response_from_supabase