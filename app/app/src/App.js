import React, { Component } from 'react'
import { HashRouter as Router, Route, Switch } from 'react-router-dom'
import { NotificationContainer } from 'react-notifications'
import { NavigationBar } from './NavigationBar'
import { SideBar } from './SideBar'
import { Auth } from './utils/Auth'
import { Layout } from './Layout'
import Home from './Home'
import { Login } from './Login'
import { Dashboard } from './Dashboard'
import { Profile } from './Profile'
import { About } from './About'
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
                    {
                        // By default, a classic navbar displays when user is logged out
                        // and a sidebar displays when it is connected.
                        //
                        // You can leave as it is or choose the one or the user, or mix both !
                        (this.state.authenticated)
                        ? <SideBar authenticated={this.state.authenticated} onAuthUpdate={this.onAuthUpdate} />
                        : <NavigationBar authenticated={this.state.authenticated} onAuthUpdate={this.onAuthUpdate} />
                    }
                    <Layout>
                        <Switch>
                            <Route exact path="/" component={Home} />
                            <Route path="/login" render={ (props) => <Login {...props} authenticated={this.state.authenticated} onAuthUpdate={this.onAuthUpdate} /> } />
                            <Route path="/dashboard" render={ (props) => <Dashboard {...props} authenticated={this.state.authenticated} /> } />
                            <Route path="/profile" render={ (props) => <Profile {...props} authenticated={this.state.authenticated} /> } />
                            <Route path="/about" component={About} />
                        </Switch>
                    </Layout>
                </Router>
            </React.Fragment>
        )
    }
}

export default App
