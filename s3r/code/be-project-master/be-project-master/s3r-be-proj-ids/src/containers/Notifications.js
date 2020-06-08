import React from "react";
import { connect } from "react-redux";
import {
    Segment,
    Table,
    Header,
    Icon,
    Statistic,
} from "semantic-ui-react";

class Notifications extends React.Component {

    componentDidUpdate() {
        // console.log('attacks state in notifications.js', this.props.attackStats);
    }

    // table to display attack notifications
    createTable = () => {
        let table = []
        let headers = [];

        // add headers to the table
        headers.push(<Table.HeaderCell>Attack Type</Table.HeaderCell>);
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
        for (let i = this.props.notifList.length - 1; i >= 0; i--) {
            let children = []
            children.push(<Table.Cell>{this.props.notifList[i]['attack.type']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.notifList[i]['frame.number']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.notifList[i]['frame.time']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.notifList[i]['frame.len']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.notifList[i]['eth.src']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.notifList[i]['eth.dst']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.notifList[i]['ip.src']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.notifList[i]['ip.dst']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.notifList[i]['ip.proto']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.notifList[i]['ip.len']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.notifList[i]['tcp.len']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.notifList[i]['tcp.srcport']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.notifList[i]['tcp.dstport']}</Table.Cell>)
            children.push(<Table.Cell>{this.props.notifList[i]['_ws.col.Info']}</Table.Cell>)
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
                        <Icon name='bell' />Attack Notifications
                    </Header>
                </Segment>

                {/* attack statistics - display number of each attack */}
                <Segment>
                    <Statistic.Group widths='five'>
                        <Statistic size='mini'>
                            <Statistic.Value>{this.props.attackStats['Wrong Setup']}</Statistic.Value>
                            <Statistic.Label>Wrong Setup</Statistic.Label>
                        </Statistic>

                        <Statistic size='mini'>
                            <Statistic.Value>{this.props.attackStats['DDOS']}</Statistic.Value>
                            <Statistic.Label>DDOS</Statistic.Label>

                        </Statistic>
                        <Statistic size='mini'>
                            <Statistic.Value>{this.props.attackStats['Data Type Probing']}</Statistic.Value>
                            <Statistic.Label>Data Type Probing</Statistic.Label>
                        </Statistic>

                        <Statistic size='mini'>
                            <Statistic.Value>{this.props.attackStats['Scan Attack']}</Statistic.Value>
                            <Statistic.Label>Scan Attack</Statistic.Label>
                        </Statistic>

                        <Statistic size='mini'>
                            <Statistic.Value>{this.props.attackStats['MITM']}</Statistic.Value>
                            <Statistic.Label>MITM</Statistic.Label>
                        </Statistic>
                    </Statistic.Group>
                </Segment>

                <Table celled>
                    {this.createTable()}
                </Table>
            </div>
        );
    }
}

export default connect(
)(Notifications);