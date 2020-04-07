import { Cookies } from 'react-cookie'
import { Notifier } from './Notifier'

export class Auth {

    constructor() {
        this.cookies = new Cookies()
        this.api_endpoint = "http://localhost:5000/api"
        this.authenticated = this.#checkUserToken()
    }

    /**
     * Returns true on valid user authentication.
     * 
     * Returns false on cookie missing or invalid properties.
     */
    isUserAuthenticated() {
        const cookie = this.cookies.get("authentication")
        if (cookie && "authenticated" in cookie)
            return cookie.authenticated
        else
            return false
    }

    /**
     * Returns false on cookie missing or invalid properties
     */
    getUserProfileCookie() {
        return this.cookies.get("profile")
    }

    /**
     * If user was successfuly authenticated by the API,
     * will register cookies including its connection
     * token and profile details.
     */
    registerUserAuthentication = (username, api_auth_query) => {
        let notify_default_response = false
        if (api_auth_query) {
            if ("error" in api_auth_query && api_auth_query.error === false) {
                // Save auth token
                this.cookies.set("authentication", {
                    "authenticated": true,
                    "token": api_auth_query.details.token,
                    "expires_at": api_auth_query.details.expires_at
                })

                // Save profile details
                // @todo TODO(flavienbwk): call profile API route
                this.cookies.set("profile", {
                    "username": username
                })
            }
            notify_default_response = true
        }
        if (notify_default_response) {
            Notifier.notifyFromResponse(api_auth_query, "Authentication")
        } else {
            Notifier.createNotification(
                "error",
                "Authentication",
                "Error while saving your session in your browser"
            )
        }
    }

    /**
     * Updates the user authentication cookies 
     * depending on token presence and validity.
     * 
     * Returns the validity status of the token. 
     */
    #checkUserToken = async () => {
        let user_authenticated = false
        let auth_cookie = this.cookies.get("authentication")
        if (auth_cookie 
            && "token" in auth_cookie 
            && "authenticated" in auth_cookie 
            && auth_cookie["authenticated"]) {
            const api_check = await this.#requestLoginCheck(auth_cookie.token)
            if (api_check === undefined || api_check.error) {
                Notifier.notifyFromResponse(api_check, "Token check", "Token check failure")
                auth_cookie = {
                    "authenticated": false,
                    "token": "",
                    "expires_at": 0
                }
            } else {
                auth_cookie["authenticated"] = true
                auth_cookie["expires_at"] = api_check.details.expires_at
                user_authenticated = true
            }
            this.cookies.set("authentication", auth_cookie)
        }
        return user_authenticated
    }

    /**
     * Returns the API response for LDAP authentication
     */
    requestLDAPLogin = (username, password) => {
        return fetch(this.api_endpoint + "/auth/ldap/login", {
            method: "POST",
            headers: { 'Content-Type': "application/json" },
            body: JSON.stringify({
                "username": username,
                "password": password
            })
        })
        .then(res => res.json())
        .then((data) => { return data })
        .catch(console.error)
    }

    /**
     * Returns the API response for LDAP authentication
     */
    #requestLoginCheck = (token_value) => {
        return fetch(this.api_endpoint + "/auth/check", {
            method: "POST",
            headers: { 'X-Api-Auth-Token': token_value }
        })
        .then(res => res.json())
        .then((data) => { return data })
        .catch(console.error)
    }

}