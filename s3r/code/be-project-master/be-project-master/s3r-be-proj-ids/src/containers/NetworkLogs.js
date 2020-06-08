import React from "react";
import { connect } from "react-redux";
import {
    Segment,
    Table,
    Header,
    Icon
} from "semantic-ui-react";

class NetworkLogs extends React.Component {

    componentDidUpdate() {
        // const netLogs = this.props.netLogs;
        // console.log('net Logs in NetworkLogs.js', netLogs);
    }

    createTable = () => {
        let table = []
        let headers = [];

        // add headers to the table - column headings
        headers.push(<Table.HeaderCell>Frame Number</Table.HeaderCell>);
        headers.push(<Table.HeaderCell>Frame Time</Table.HeaderCell>);
        headers.push(<Table.HeaderCell>Frame Length</Table.HeaderCell>);
        headers.push(<Table.HeaderCell>Mac Source</Table.HeaderCell>);
        headers.push(<Table.HeaderCell>Mac Dest</Table.HeaderCell>);
        headers.push(<Table.HeaderCell>IP Source</Table.HeaderCell>);
        headers.push(<Table.HeaderCell>IP Dest</Table.HeaderCell>);
        headers.push(<Table.HeaderCell>IP Protocol</Table.HeaderCell>);
        headers.push(<Table.HeaderCell>IP Length</Table.HeaderCell>);
        headers.push(<Table.HeaderCell>TCP Length</Table.HeaderCell>);
        headers.push(<Table.HeaderCell>TCP Source Port</Table.HeaderCell>);
        headers.push(<Table.HeaderCell>TCP Dest Port</Table.HeaderCell>);
        headers.push(<Table.HeaderCell>Info</Table.HeaderCell>);
        table.push(<Table.Header><Table.Row>{headers}</Table.Row></Table.Header>);

        // Outer loop to create parent
        for (let i = this.props.netLogs.length - 1; i >= 0; i--) {
            let children = []
            // push children - add column values here
            children.push(<Table.Cell>{this.props.netLogs[i]['frame.number']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.netLogs[i]['frame.time']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.netLogs[i]['frame.len']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.netLogs[i]['eth.src']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.netLogs[i]['eth.dst']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.netLogs[i]['ip.src']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.netLogs[i]['ip.dst']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.netLogs[i]['ip.proto']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.netLogs[i]['ip.len']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.netLogs[i]['tcp.len']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.netLogs[i]['tcp.srcport']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.netLogs[i]['tcp.dstport']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.netLogs[i]['_ws.col.Info']}</Table.Cell>)
            //Create the parent and add the children
            table.push(<Table.Body><Table.Row children={children} /></Table.Body>)
        }

        return table
    }

    render() {
        return (
            <div style={{ marginLeft: '3em', marginRight: '3em' }}>
                <Segment style={{ marginTop: '4em', textAlign: "center" }} vertical>
                    <Header as='h3'>
                        <Icon name='connectdevelop' />Network Logs
                    </Header>
                </Segment>
                <Table celled>
                    {this.createTable()}
                </Table>
            </div>
        );
    }
}

export default connect(
)(NetworkLogs);