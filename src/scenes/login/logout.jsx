//import React from 'react'

export default function Logout() {
    const currentUrl = window.location.origin + "/";
    window.localStorage.clear();
    window.location.href = currentUrl + "login";
    return
}
