import React from 'react';
import { HashRouter as Router, Route, Switch } from 'react-router-dom';
import { Login } from './Login';
import Home from './Home';
import { About } from './About';
import { Layout } from './Layout';
import { NavigationBar } from './NavigationBar';
import packageJson from '../package.json';

function App() {

    return (
        <React.Fragment>
            <Router basename={packageJson["homepage"] + "/"}>
                <NavigationBar />
                <Layout>
                    <Switch>
                        <Route exact path="/" component={Home} />
                        <Route path="/login" component={Login} />
                        <Route path="/about" component={About} />
                    </Switch>
                </Layout>
            </Router>
        </React.Fragment>
    );
}

export default App;
