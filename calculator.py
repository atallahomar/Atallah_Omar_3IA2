from mcp.server.fastmcp import FastMCP


mcp = FastMCP(name="MyCalculator")

@mcp.tool()
def addition(a: float, b: float) -> float:
    return a + b

@mcp.tool()
def soustraction(a: float, b: float) -> float:
    return a - b

@mcp.tool()
def multiplication(a: float, b: float) -> float:
    return a * b

@mcp.tool()
def division(a: float, b: float) -> float:
    if b == 0:
        return "Erreur : division par zéro."
    return a / b

if __name__ == "__main__":
    mcp.run(transport="stdio")