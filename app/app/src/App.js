import React, { Component } from 'react';
import { HashRouter as Router, Route, Switch } from 'react-router-dom';
import { Auth } from './utils/Auth'
import { Login } from './Login';
import Home from './Home';
import { About } from './About';
import { Layout } from './Layout';
import { NavigationBar } from './NavigationBar';
import packageJson from '../package.json';

export class App extends Component {

    constructor(props) {
        super(props)
        this.auth = new Auth([this.onAuthUpdate])
        this.auth.checkUserToken()
        this.state = {
            "authenticated": this.auth.isUserAuthenticated()
        }
    }

    /**
     * Component <Login> will trigger this parent event to
     * inform other routes (<NavigationBar> for example),
     * that authentication information have been updated.
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
                    <NavigationBar authenticated={this.state.authenticated} />
                    <Layout>
                        <Switch>
                            <Route exact path="/" component={Home} />
                            <Route path="/login" render={ (props) => <Login {...props} onAuthUpdate={this.onAuthUpdate} /> } />
                            <Route path="/about" component={About} />
                        </Switch>
                    </Layout>
                </Router>
            </React.Fragment>
        )
    }
}

export default App;
