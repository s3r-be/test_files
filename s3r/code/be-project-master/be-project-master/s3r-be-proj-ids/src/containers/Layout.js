import React from "react";
import {
  Container,
  Divider,
  Grid,
  Header,
  Image,
  List,
  Menu,
  Segment,
  Icon
} from "semantic-ui-react";
import { Link, withRouter } from "react-router-dom";
import { connect } from "react-redux";
import { logout } from "../store/actions/auth";

class CustomLayout extends React.Component {

  render() {
    const { authenticated } = this.props;
    return (
      <div>
        <Menu fixed="top" inverted>
          <Container>
            <Link to="/">
              <Menu.Item header><Icon inverted name='home' /> Home</Menu.Item>
            </Link>
            {authenticated ? (
              <React.Fragment>
                <Menu.Item header onClick={() => this.props.logout()}>
                  <Icon inverted name='log out' /> Logout
                </Menu.Item>
                <Link to="/networkLogs">
                  <Menu.Item header><Icon inverted name='connectdevelop' /> Network Logs</Menu.Item>
                </Link>
                <Link to="/dashboard">
                  <Menu.Item header><Icon inverted name='dashboard' /> Dashboard</Menu.Item>
                </Link>
                <Link to="/visualisations">
                  <Menu.Item header><Icon inverted name='line graph' /> Visualisations</Menu.Item>
                </Link>
                <Link to="/notifications">
                  <Menu.Item header><Icon inverted name='bell' /> Notifications</Menu.Item>
                </Link>
              </React.Fragment>
            ) : (
                <React.Fragment>
                  <Link to="/login">
                    <Menu.Item header><Icon inverted name='sign-in' /> Login</Menu.Item>
                  </Link>
                  <Link to="/signup">
                    <Menu.Item header><Icon inverted name='signup' /> Signup</Menu.Item>
                  </Link>
                  <Link to="/networkLogs">
                    <Menu.Item header><Icon inverted name='connectdevelop' /> Network Logs</Menu.Item>
                  </Link>
                  <Link to="/dashboard">
                    <Menu.Item header><Icon inverted name='dashboard' /> Dashboard</Menu.Item>
                  </Link>
                  <Link to="/visualisations">
                    <Menu.Item header><Icon inverted name='line graph' /> Visualisations</Menu.Item>
                  </Link>
                  <Link to="/notifications">
                    <Menu.Item header><Icon inverted name='bell' /> Notifications</Menu.Item>
                  </Link>
                </React.Fragment>
              )}
          </Container>
        </Menu>

        {this.props.children}

        <Segment
          inverted
          vertical
          style={{ margin: "5em 0em 0em", padding: "5em 0em" }}
        >
          <Container textAlign="center">
            <Grid divided inverted stackable>
              <Grid.Column width={3}>
                <Header inverted as="h4" content="Group 1" />
                <List link inverted>
                  <List.Item as="a">Link One</List.Item>
                  <List.Item as="a">Link Two</List.Item>
                  <List.Item as="a">Link Three</List.Item>
                  <List.Item as="a">Link Four</List.Item>
                </List>
              </Grid.Column>
              <Grid.Column width={3}>
                <Header inverted as="h4" content="Group 2" />
                <List link inverted>
                  <List.Item as="a">Link One</List.Item>
                  <List.Item as="a">Link Two</List.Item>
                  <List.Item as="a">Link Three</List.Item>
                  <List.Item as="a">Link Four</List.Item>
                </List>
              </Grid.Column>
              <Grid.Column width={3}>
                <Header inverted as="h4" content="Group 3" />
                <List link inverted>
                  <List.Item as="a">Link One</List.Item>
                  <List.Item as="a">Link Two</List.Item>
                  <List.Item as="a">Link Three</List.Item>
                  <List.Item as="a">Link Four</List.Item>
                </List>
              </Grid.Column>
              <Grid.Column width={7}>
                <Header inverted as="h4" content="Footer Header" />
                <p>
                  Extra space for a call to action inside the footer that could
                  help re-engage users.
                </p>
              </Grid.Column>
            </Grid>

            <Divider inverted section />
            <Image centered size="mini" src="/logo.png" />
            <List horizontal inverted divided link size="small">
              <List.Item as="a" href="#">
                Site Map
              </List.Item>
              <List.Item as="a" href="#">
                Contact Us
              </List.Item>
              <List.Item as="a" href="#">
                Terms and Conditions
              </List.Item>
              <List.Item as="a" href="#">
                Privacy Policy
              </List.Item>
            </List>
          </Container>
        </Segment>
      </div>
    );
  }
}

const mapStateToProps = state => {
  return {
    authenticated: state.auth.token !== null
  };
};

const mapDispatchToProps = dispatch => {
  return {
    logout: () => dispatch(logout())
  };
};

export default withRouter(
  connect(
    mapStateToProps,
    mapDispatchToProps
  )(CustomLayout)
);
