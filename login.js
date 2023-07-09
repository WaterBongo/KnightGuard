const processEvent = (mutationList, observer) => {
  for (const atag of document.getElementsByTagName("a")) {
    if (atag.href.indexOf("clerk.com") > -1) {
      atag.parentElement.remove();
    }
  }
};

new MutationObserver(processEvent).observe(document, {childList: true, subtree: true});

function handleLogin(information) {
  if (information["user"]) {
    document.getElementById("sign_in").setAttribute("style", "display: none !important;");
    document.getElementById("user-button").setAttribute("style", "margin-right: 5px !important;");
    window.Clerk.mountUserButton(document.getElementById("user-button"), {afterSignOutUrl: "/"});
  }
}

var clerkjs = document.createElement("script");
clerkjs.setAttribute("crossorigin", "anonymous");
clerkjs.setAttribute("data-clerk-publishable-key", "pk_test_aW52aXRpbmctc3VuYmlyZC02MS5jbGVyay5hY2NvdW50cy5kZXYk");
clerkjs.setAttribute("async", "");
clerkjs.setAttribute("type", "text/javascript");
clerkjs.setAttribute("src", "https://inviting-sunbird-61.clerk.accounts.dev/npm/@clerk/clerk-js@4/dist/clerk.browser.js");
clerkjs.addEventListener('load', async function(){
  await window.Clerk.load();
  window.Clerk.addListener(handleLogin);
});
document.head.appendChild(clerkjs);