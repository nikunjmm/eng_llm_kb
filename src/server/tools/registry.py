from typing import Callable, Dict, Any, List

def get_equipment_details(equipment_id: str) -> str:
    """Finds manufacturing equipment details from the knowledge base by ID."""
    # Dummy mock implementation
    if "PUMP" in equipment_id:
        return f'{{"id": "{equipment_id}", "type": "Centrifugal", "max_pressure": 150, "status": "active"}}'
    return f'{{"error": "Equipment {equipment_id} not found in knowledge base."}}'

# We prefix with 'client_' to signal the core_agent loop that execution happens on the C# side
def client_set_operating_pressure(equipment_id: str, pressure_psi: int) -> str:
    """Proposes an action to update the operating pressure of a piece of equipment in the native C# application."""
    # Because it starts with 'client_', the agent loop will pause, return an ActionRequest, and not execute this
    return ""

def get_tool_definitions() -> List[Callable]:
    """Returns all native functions mapped as tools for the Gemini SDK"""
    return [get_equipment_details, client_set_operating_pressure]

def execute_tool(function_name: str, args_dict: Dict[str, Any]) -> Any:
    """Executes a server-side tool given its name and dictionary of arguments."""
    registry = {
        "get_equipment_details": get_equipment_details
    }
    
    if function_name in registry:
        return registry[function_name](**args_dict)
    
    raise ValueError(f"Unknown server-side tool: {function_name}")
