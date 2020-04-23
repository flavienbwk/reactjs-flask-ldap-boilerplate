import React, { Component } from 'react'
import packageJson from '../package.json';

export class About extends Component {

    render() {
        return (
            <div>
                <h2>About</h2>
                <p>This app is a free and open-source <a target="_blank" rel="noopener noreferrer" href="https://github.com/flavienbwk/reactjs-flask-ldap-docker-boilerplate">boilerplate</a> brought to you by <a target="_blank" rel="noopener noreferrer" href="https://flavien.berwick.fr/en">Flavien Berwick</a>.</p>
                <p>If you find an issue or have a suggestion, <a target="_blank" rel="noopener noreferrer" href="https://github.com/flavienbwk/reactjs-flask-ldap-docker-boilerplate/issues">please open an issue on Github</a>.</p>
                <hr />
                <p>Version <b>{packageJson["version"]}</b></p>
            </div>
        )
    }

    componentDidMount() {
        document.title = "About - My Project";
    }

}
