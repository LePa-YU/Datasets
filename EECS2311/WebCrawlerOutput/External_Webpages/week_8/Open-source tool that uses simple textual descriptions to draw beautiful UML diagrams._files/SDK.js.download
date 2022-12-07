/* eslint-disable no-console,no-bitwise,no-plusplus,no-useless-escape */
/* eslint-env browser */
window.pushmaster = {
  enableOverlay: false,
  swPath: '/sw.js',
  swScope: '/',
  userPromptInterval: 30, // in mins
  ingestPath: 'https://in.pushmaster-in.xyz/',
  cdnPath: 'https://cdn.pushmaster-cdn.xyz/scripts/',
  promptTrackSplit: 0.1,
  ...window.pushMST_config,
};

async function promptEventTrack(promptEvent, err) {
  function isTrackingEnabled() {
    let promptTrack;
    let isNewPromptTrack = false;

    if (window.pushmaster.promptTrack) {
      promptTrack = window.pushmaster.promptTrack;
    } else {
      promptTrack = localStorage.getItem('push_promptTrack');
      if (promptTrack === null) {
        const samplingProbability = window.pushmaster.promptTrackSplit || 0.1;
        isNewPromptTrack = true;
        if (Math.random() < samplingProbability) {
          promptTrack = true;
        } else {
          promptTrack = false;
        }
      }
      window.pushmaster.promptTrack = promptTrack;

      if (isNewPromptTrack === true) {
        localStorage.setItem('push_promptTrack', promptTrack);
      }
    }

    return promptTrack;
  }

  function getVisitorUUID() {
    function createNewUUID() {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = (Math.random() * 16) | 0;
        const v = c === 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
      });
    }

    if (window.pushmaster.uuid) {
      return window.pushmaster.uuid;
    }

    let uuid = localStorage.getItem('push_uuid');
    let isNewUUID = false;
    if (!uuid) {
      uuid = createNewUUID();
      isNewUUID = true;
    }

    window.pushmaster.uuid = uuid;

    if (isNewUUID === true) {
      localStorage.setItem('push_uuid', uuid);
    }
    return uuid;
  }

  if (window.pushmaster.lastEventTrigered) {
    // we avoid pararrell execution of transactions with localstorage
    const minWaitTime = 300; // in ms
    const timeSinceLastTransaction = Date.now() - window.pushmaster.lastEventTrigered;
    if (timeSinceLastTransaction < minWaitTime) {
      const timeToWait = timeSinceLastTransaction - minWaitTime; // in ms

      // wait for timeToWait ms before continuing with execution
      await new Promise((res) => {
        setTimeout(res, timeToWait);
      });
    }
  }
  window.pushmaster.lastEventTrigered = Date.now();

  // check if tracking enabled before sending events
  if (isTrackingEnabled()) {
    const visitorUUID = getVisitorUUID();
    const serverEndpoint = `${window.pushmaster.ingestPath}prompt`;
    const fetchBody = {
      eventType: promptEvent,
      href: window.location.href,
      ua: navigator.userAgent,
      ts: Date.now(),
      uuid: visitorUUID,
      promptId: window.pushmaster.i18n && window.pushmaster.i18n.promptId,
      promptTrackSplit: window.pushmaster.promptTrackSplit,
    };
    if (err) {
      const errString = `${err.toString()} - ${JSON.stringify(err, Object.getOwnPropertyNames(err))}`;
      fetchBody.err = errString;
    }

    const fetchHeaders = new Headers();
    fetchHeaders.append('Content-Type', 'application/json');

    fetch(serverEndpoint, {
      method: 'POST',
      body: JSON.stringify(fetchBody),
      mode: 'cors',
      headers: fetchHeaders,
    }).catch((error) => console.error(error));
  }
}

const promptCall = (callText) => async (err) => {
  promptEventTrack(callText, err);
};

const pushPrompt = {
  onDenied: promptCall('onDenied'),
  onCanceled: promptCall('onCanceled'),
  onGranted: promptCall('onGranted'),
  onAlreadySubscribed: promptCall('onAlreadySubscribed'),
  onAlreadyDenied: promptCall('onAlreadyDenied'),
  onManualCloseOverlay: promptCall('onManualCloseOverlay'),
  onUnsupported: promptCall('onUnsupported'),
  onResubscribed: promptCall('onResubscribed'),
  onError: promptCall('onError'),
};

function addOverlay() {
  if (!window.pushmaster.enableOverlay) return;
  return new Promise(function (resolve) {
    setTimeout(function () {
      const n = document.createElement('script');
      n.src = `${window.pushmaster.cdnPath}templates/overlay_v2.min.js`;
      document.body.appendChild(n);
      resolve();
    }, 0);
  });
}

function removeOverlay() {
  // eslint-disable-next-line no-unused-expressions
  document.getElementById('pushMST_overlay') && document.getElementById('pushMST_overlay').remove();
}

window.manualCloseOverlay = () => {
  removeOverlay();
  Promise.all([pushPrompt.onManualCloseOverlay()]);
};

function isFirefox() {
  return navigator.userAgent.toLowerCase().indexOf('firefox') > -1;
}

function isDevicePushCompatible() {
  if (!('serviceWorker' in navigator)) {
    return false;
  }

  if (typeof Notification === 'undefined') {
    return false;
  }

  // https://stackoverflow.com/a/31732310
  const isSafari =
    navigator.vendor &&
    navigator.vendor.indexOf('Apple') > -1 &&
    navigator.userAgent &&
    navigator.userAgent.indexOf('CriOS') === -1 &&
    navigator.userAgent.indexOf('FxiOS') === -1;

  const isIos =
    ['iPad Simulator', 'iPhone Simulator', 'iPod Simulator', 'iPad', 'iPhone', 'iPod'].includes(navigator.platform) ||
    // iPad on iOS 13 detection
    (navigator.userAgent.includes('Mac') && 'ontouchend' in document);

  const isMobile = function () {
    const a = navigator.userAgent || navigator.vendor || window.opera;
    return (
      /(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(
        a
      ) ||
      /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(
        a.substr(0, 4)
      )
    );
  };

  // based on https://stackoverflow.com/a/50195587
  const isTablet = function () {
    const a = navigator.userAgent || navigator.vendor || window.opera;
    return /(ipad|tablet|(android(?!.*mobile))|(windows(?!.*phone)(.*touch))|kindle|playbook|silk|(puffin(?!.*(IP|AP|WP))))/i.test(
      a
    );
  };

  const isMobileOrTablet = function () {
    return isMobile() || isTablet();
  };

  // based on https://stackoverflow.com/a/31609308
  const isOpera = function () {
    const isChromium = window.chrome;
    const isOperaBrowser =
      window.navigator.userAgent.indexOf('OPR') > -1 || window.navigator.userAgent.indexOf('Opera') > -1;
    return isChromium !== null && isOperaBrowser === true;
  };

  // https://stackoverflow.com/a/66486912
  const isEdge = function () {
    return /Edg/.test(navigator.userAgent);
  };

  // if (device in ['mobile', 'tablet']) and (browser in ['edge', 'opera', 'firefox']): prompt_user = False
  const isExcludedDevice = function () {
    return isMobileOrTablet() && (isFirefox() || isOpera() || isEdge());
  };

  // no support for Safari or iOS
  // no support if no Notification
  if (isSafari || isIos || isExcludedDevice()) {
    return false;
  }

  return true;
}

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

async function notificationServerSync(notificationObject) {
  if (!notificationObject) {
    return;
  }

  try {
    const serverEndpoint = `${window.pushmaster.ingestPath}subscriptions`;
    const currentSubscriptionId = localStorage.getItem('pushMST_subscriptionId') || null;
    const currentSubscriberId = localStorage.getItem('pushMST_subscriberId') || null;

    const fetchBody = {};
    fetchBody.notificationObject = notificationObject;
    fetchBody.subscriberId = currentSubscriberId;
    fetchBody.subscriptionId = currentSubscriptionId;
    fetchBody.browserHost = window.location.host;
    fetchBody.browserHref = window.location.href;
    fetchBody.browserLanguage = navigator.language;
    fetchBody.browserLanguages = navigator.languages;

    const fetchHeaders = new Headers();
    fetchHeaders.append('Content-Type', 'application/json');

    // Register notificationObject in server
    const response = await fetch(serverEndpoint, {
      method: 'POST',
      body: JSON.stringify(fetchBody),
      mode: 'cors',
      headers: fetchHeaders,
    });

    const resBody = await response.json();
    if (response.ok) {
      localStorage.setItem('pushMST_subscriberId', resBody.data.subscriberId);
      localStorage.setItem('pushMST_subscriptionId', resBody.data.subscriptionId);
      // console.log(resBody);
    } else {
      console.log('resBody not ok in notificationServerSync()');
    }
  } catch (err) {
    await pushPrompt.onError(err);
  }
}

async function pushFlow() {
  function isPromptEnabled() {
    // this function manages the frequency at which a user is prompted, returns true if we should update.
    const lastUserPrompt = parseInt(localStorage.getItem('pushMST_lastUserPrompt'), 10) || 0;
    const timeSinceLastUserPrompt = (Date.now() - lastUserPrompt) / (1000 * 60); // in minutes

    if (timeSinceLastUserPrompt > window.pushmaster.userPromptInterval) {
      // in this case we will presumably prompt the user, so we will update the stored last updated date.
      localStorage.setItem('pushMST_lastUserPrompt', Date.now()); // update the last prompt ts
      return true;
    }

    // in this case the user won't be prompted, so we don't update the lastPrompted variable
    return false;
  }

  async function subscribeAndSync(register, alreadySubscribed = false, subscription) {
    /**
     * This function checks if the users has granted Notification permissions.
     * - If the permission is granted, we will subscribe the user with the browser and update our server.
     * - Else, we just print a message in the console.
     */

    const { permission } = Notification;
    const subscriptionOptions = {
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(window.pushmaster.vapidPK),
    };

    if (permission === 'granted') {
      let notificationObject;
      let resubscribed = false;
      try {
        notificationObject = await register.pushManager.subscribe(subscriptionOptions);
      } catch (e) {
        if (subscription) {
          await subscription.unsubscribe();
          notificationObject = await register.pushManager.subscribe(subscriptionOptions);
          resubscribed = true;
        }
      }
      await notificationServerSync(notificationObject);
      if (!alreadySubscribed && !resubscribed) {
        await pushPrompt.onGranted();
      } else if (resubscribed) {
        await pushPrompt.onResubscribed();
      }
    } else if (permission === 'default') {
      await pushPrompt.onCanceled();
    } else {
      await pushPrompt.onDenied();
    }
  }

  // register sw
  try {
    let register;
    try {
      register = await navigator.serviceWorker.register(window.pushmaster.swPath, {
        scope: window.pushmaster.swScope,
      });
    } catch (err) {
      if (err instanceof DOMException && err.name === 'SecurityError')
        register = await navigator.serviceWorker.register(`https://${window.location.hostname}${window.pushmaster.swPath}`, {
          scope: `https://${window.location.hostname}${window.pushmaster.swScope}`,
        });
      else {
        // if it wasn't the hostname mismatch, we pass on the error
        throw err;
      }
    }

    // wait until sw is ready
    register = await navigator.serviceWorker.ready;

    // only do an overlay if we have no permission setting and haven't asked recently
    if (isPromptEnabled()) {
      if (Notification.permission === 'default' || Notification.permission == null) {
        // firefox handled separately
        if (isFirefox()) {
          document.addEventListener(
            'click',
            async function (e) {
              e.preventDefault();
              addOverlay();
              await Notification.requestPermission();
              removeOverlay();
              await subscribeAndSync(register);
            },
            { once: true } // not available in IE
          );
        } else {
          addOverlay();
          await Notification.requestPermission();
          removeOverlay();
          await subscribeAndSync(register);
        }
      } else if (Notification.permission === 'granted') {
        // if we already granted before but lost the subscription, show no overlay but resubscribe
        const subscription = await register.pushManager.getSubscription();
        if (!subscription) {
          await subscribeAndSync(register, true);
        } else if (!localStorage.getItem('pushMST_subscriptionId')) {
          await subscribeAndSync(register, false, subscription);
        }
        await pushPrompt.onAlreadySubscribed();
      } else if (Notification.permission === 'denied') {
        await pushPrompt.onAlreadyDenied();
      }
    }
  } catch (err) {
    await pushPrompt.onError(err);
  }
}

promptEventTrack('pv');

// Check for service worker
if (isDevicePushCompatible() === true) {
  (() => {
    const getConsentData = (cb) => {
      if (typeof __tcfapi !== 'function') throw new Error('No consent module.');
      // eslint-disable-next-line no-undef
      __tcfapi('getTCData', 2, (data) => cb(data));
    };
    const addConsentListener = (cb) => {
      if (typeof __tcfapi !== 'function') throw new Error('No consent module.');
      // eslint-disable-next-line no-undef
      __tcfapi('addEventListener', 2, (data) => cb(data));
    };

    try {
      const indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB;
      if (indexedDB) {
        const dbName = 'pushmaster';
        const storeName = 'consent';
        const version = 1; // versions start at 1
        // eslint-disable-next-line security/detect-non-literal-fs-filename
        const request = indexedDB.open(dbName, version);
        request.onupgradeneeded = () => request.result.createObjectStore(storeName);
        request.onsuccess = () => {
          const saveConsent = (consentData) => {
            const db = request.result;
            const tx = db.transaction(storeName, 'readwrite');
            const store = tx.objectStore(storeName);
            store.put({ ...consentData, ts: new Date() }, 'consent');
            return tx.complete;
          };
          try {
            getConsentData(saveConsent);
            addConsentListener(saveConsent);
            // eslint-disable-next-line no-empty
          } catch (e) {}
        };
      }
      // eslint-disable-next-line no-empty
    } catch (e) {}
  })();

  pushFlow().catch((err) => {
    removeOverlay();
    Promise.all([pushPrompt.onError(err)]);
    console.error(err);
  });
} else {
  Promise.all([pushPrompt.onUnsupported()]);
}
