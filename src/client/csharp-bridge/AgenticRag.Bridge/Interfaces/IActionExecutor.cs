using System.Threading.Tasks;

namespace AgenticRag.Bridge.Interfaces
{
    /// <summary>
    /// Contract for an object that can execute actions proposed by the LLM.
    /// The host application implements this.
    /// </summary>
    public interface IActionExecutor
    {
        /// <summary>
        /// Executes a specific tool/action securely in the host ap.
        /// </summary>
        /// <param name="actionName">The name of the action (e.g. set_operating_pressure)</param>
        /// <param name="parametersJson">The JSON parameters provided by the LLM.</param>
        /// <returns>A string response indicating the result of the action.</returns>
        Task<string> ExecuteActionAsync(string actionName, string parametersJson);
    }
}
