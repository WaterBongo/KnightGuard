document.getElementById('panic').onclick = async function() {
    new Notify({
        status: 'success',
        title: 'Success',
        text: 'Authorities have been notified and surrounding employees have been alerted.',
        effect: 'fade',
        speed: 300,
        customClass: '',
        customIcon: '',
        showIcon: true,
        showCloseButton: true,
        autoclose: false,
        autotimeout: 3000,
        gap: 20,
        distance: 20,
        type: 1,
        position: 'right top'
    })
    const e = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {enableHighAccuracy: false, timeout: 5000, maximumAge: 0})
    });
    await fetch('/panic', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({long: e.coords.longitude, lat: e.coords.latitude})
    });
}