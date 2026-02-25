using System;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using AgenticRag.Bridge.Interfaces;

namespace AgenticRag.Bridge.Interop
{
    /// <summary>
    /// The primary class exposed to WebView2 for Javascript-to-C# communication.
    /// Must be registered using webView.CoreWebView2.AddHostObjectToScript.
    /// </summary>
    [ClassInterface(ClassInterfaceType.AutoDual)]
    [ComVisible(true)]
    public class WebView2Interop
    {
        private readonly IContextExtractor _contextExtractor;
        private readonly IActionExecutor _actionExecutor;

        public WebView2Interop(IContextExtractor contextExtractor, IActionExecutor actionExecutor)
        {
            _contextExtractor = contextExtractor ?? throw new ArgumentNullException(nameof(contextExtractor));
            _actionExecutor = actionExecutor ?? throw new ArgumentNullException(nameof(actionExecutor));
        }

        // --- Methods Invoked By React UI via window.chrome.webview.hostObjects ---

        /// <summary>
        /// Called by React to grab the live active context before sending a prompt to the FastAPI server.
        /// </summary>
        public string GetLiveContext()
        {
            try
            {
                 // Interop methods need to return synchronously or use async patterns compatible with WebView2
                 return _contextExtractor.GetCurrentScreenContextAsync().GetAwaiter().GetResult();
            }
            catch (Exception ex)
            {
                 return $"{{\"error\": \"{ex.Message}\"}}";
            }
        }

        /// <summary>
        /// Called by React when the user clicks 'Approve Action' on an LLM proposal.
        /// </summary>
        public string DispatchAction(string actionName, string parametersJson)
        {
            try
            {
                 return _actionExecutor.ExecuteActionAsync(actionName, parametersJson).GetAwaiter().GetResult();
            }
            catch (Exception ex)
            {
                 return $"{{\"error\": \"Failed to execute action: {ex.Message}\"}}";
            }
        }
    }
}
