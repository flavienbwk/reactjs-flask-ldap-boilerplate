import React, { Component } from 'react'
import { HashRouter as Router, Route, Switch } from 'react-router-dom'
import { NotificationContainer } from 'react-notifications'
import { Auth } from './utils/Auth'
import { Login } from './Login'
import Home from './Home'
import { About } from './About'
import { Dashboard } from './Dashboard'
import { Layout } from './Layout'
import { NavigationBar } from './NavigationBar'
import packageJson from '../package.json'

export class App extends Component {

    constructor(props) {
        super(props)
        this.auth = new Auth([this.onAuthUpdate])
        this.auth.checkUserToken()
        this.state = {
            "authenticated": this.auth.isUserAuthenticated()
        }
        this.periodicLoginCheck(60)
    }

    /**
     * Periodically checks for user authentication
     * 
     * @param {int} seconds 
     */
    periodicLoginCheck(seconds = 60) {
        const interval = setInterval(() => {
            if (this.state.authenticated)
                this.auth.checkUserToken()
        }, seconds * 1000);
        return () => clearInterval(interval);
    };

    /**
     * Child components may trigger this parent event to
     * inform other routes (<NavigationBar> for example),
     * that authentication information have been updated.
     * 
     * This allows to show the "Login" or "Logout" button
     * depending on user's authentication status.
     */
    onAuthUpdate = () => {
        this.setState({
            "authenticated": this.auth.isUserAuthenticated()
        })
    }

    render() {
            return (
            <React.Fragment>
                <Router basename={packageJson["homepage"] + "/"}>
                    <NotificationContainer />
                    <NavigationBar authenticated={this.state.authenticated} onAuthUpdate={this.onAuthUpdate} />
                    <Layout>
                        <Switch>
                            <Route exact path="/" component={Home} />
                            <Route path="/login" render={ (props) => <Login {...props} authenticated={this.state.authenticated} onAuthUpdate={this.onAuthUpdate} /> } />
                            <Route path="/dashboard" render={ (props) => <Dashboard {...props} authenticated={this.state.authenticated} /> } />
                            <Route path="/about" component={About} />
                        </Switch>
                    </Layout>
                </Router>
            </React.Fragment>
        )
    }
}

export default App
