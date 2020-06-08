import React from 'react';
import Background from '../Images/Dashboard/1.png';
import img from '../Images/Dashboard/car.png';
import { connect } from "react-redux";
import axios from 'axios';
import {
    Segment,
    Header,
    Icon
} from "semantic-ui-react";

var sectionStyle = {
    width: "100%",
    height: "900px",
    backgroundImage: `url(${Background})`, // main background file
    paddingLeft: "0px"
};

var movingAvg = [];
var smoothingWindow = 10;

class Imgg extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            pos: 0
        }

        // get socket for notification
        this.phpSocket = this.props.phpSocket;
    }

    async sleep() {
        await new Promise(r => setTimeout(r, 1000));
    }

    componentDidMount() {

        this.phpSocket.onopen = (e) => {
            // send message to initiate notification data transfer
            this.phpSocket.send(JSON.stringify({
                'message': 'initiate node data transfer'
            }))
        }

        this.phpSocket.onmessage = (e) => {
            //console.log(e.data);
            // var data = JSON.parse(e.data);
            // appending received message to state
            this.writearray(e.data);
            //  console.log(data);
            // console.log('state netLogs: ', this.state.netLogs);
        };

        // on closing web socket
        this.phpSocket.onclose = (e) => {
            console.error('Php socket closed unexpectedly');

            // setTimeout(function () {
            //     console.log('Reconnecting to websocket: ' + '0.0.0.0:12345');
            //     this.phpSocket = new WebSocket(
            //         'ws://' + "0.0.0.0:12345");
            //     console.log(this.phpSocket);
            // }, 5000);

            // for (let count = 0; count < 15 && this.phpSocket.readyState !== WebSocket.OPEN; count++) {
            //     // this.sleep();

            //     // console.log(this.phpSocket);
            //     setTimeout(function () {
            //         console.log('Reconnecting to websocket: ' + '0.0.0.0:12345 - ' + count);
            //         this.phpSocket = new WebSocket(
            //             'ws://' + "0.0.0.0:12345");
            //     }, 2000);

            // }
            // if (this.phpSocket.readyState === WebSocket.OPEN) {
            //     this.phpSocket.send(JSON.stringify({
            //         'message': 'initiate node data transfer'
            //     }))
            // } else {
            //     console.error('Max reconnection attempt reached.');
            // }
            // console.log(this.phpSocket);
        };
    }

    writearray = (d) => {

        d = d.split('\n', 10);
        //console.log(d);
        d = Number(d[0]);
        // console.log('data', d, 'type of data ', typeof d, 'smoothingWindow', smoothingWindow);
        // append to array
        movingAvg.push(d)
        // console.log(movingAvg);

        if (movingAvg.length >= smoothingWindow) {
            // removes first value if length reaches smoothing window (eg 10)
            movingAvg.shift();
        }
        // get sum
        var tempAvg = 0;
        // console.log('tempAvg: ' + tempAvg + ' movingAvg ', movingAvg);
        movingAvg.forEach(element => {
            tempAvg += element;
        });
        // console.log("Sum"+tempAvg);
        // get average
        tempAvg /= movingAvg.length;
        // console.log("Avg"+tempAvg);
        // condition for tempAvg going beyond threshold
        if (tempAvg > 1000) {
            tempAvg = tempAvg % 1000;
        }
        this.setState({
            pos: tempAvg
        });
        // console.log('tempAvg: ' + tempAvg);
        // console.log('tempAvg: ' + tempAvg + '--pos: ' + this.state.pos);

    }

    updateData = () => {
        axios.get('http://localhost/ids/getData.php')
            .then((data) => {
                // console.log(data);
                this.writearray(data.data);
            })
    }

    render() {
        return (
            <div id="sdf">

                <Segment style={{ marginTop: '4em', textAlign: "center" }} vertical>
                    <Header as='h3'>
                        <Icon name='dashboard' />Dashboard
                    </Header>
                </Segment>

                <div style={sectionStyle}>
                    <div >
                        <img src={img} alt="car" width="600" style={{ top: "500px", left: this.state.pos + "px", position: "relative" }} />
                    </div>
                    <h1>Position = {this.state.pos}</h1>
                </div>
            </div>
        );
    }
}

export default connect(
)(Imgg);
