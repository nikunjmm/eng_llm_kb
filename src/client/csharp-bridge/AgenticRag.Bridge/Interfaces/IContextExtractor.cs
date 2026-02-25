using System.Threading.Tasks;

namespace AgenticRag.Bridge.Interfaces
{
    /// <summary>
    /// Contract for an object that can extract context from the host Windows application.
    /// The host application implements this and passes it to the Bridge.
    /// </summary>
    public interface IContextExtractor
    {
        /// <summary>
        /// Retrieves the current screen's semantic context as a JSON string.
        /// </summary>
        Task<string> GetCurrentScreenContextAsync();
    }
}
