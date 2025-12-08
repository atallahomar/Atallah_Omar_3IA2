from mcp.server.fastmcp import FastMCP
mcp=FastMCP(
    name="sayhello"
)
@mcp.tool()
def say_hello(name):
    """say hello to a user"""
    return f"Hello to {name}!"



if __name__ == "__main__":
    mcp.run(transport="stdio")
