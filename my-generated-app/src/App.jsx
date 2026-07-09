import React from 'react';
import { ThemeProvider } from '@mui/system';
import { Box, Typography, IconButton, Grid, Paper } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import UserIcon from '@mui/icons-material/Person';
import MonitorIcon from '@mui/icons-material/Laptop';
import DollarSignIcon from '@mui/icons-material/MoneyOffCsRed';
import NotificationImportantIcon from '@mui/icons-material/NotificationImportant';

const AppWrapper = ({ theme }) => (
  <ThemeProvider theme={theme}>
    <Box
      display="flex"
      flexDirection="column"
      minHeight="100vh"
      bg="#121212"
      color="white"
    >
      <DashboardPage />
      <footer>
        <Typography variant="body2" align="center">
          © 2023 Company Name. Built with React and Tailwind CSS
        </Typography>
      </footer>
    </Box>
  </ThemeProvider>
);

const DashboardPage = () => (
  <Grid container spacing={3}>
    <Grid item xs={12} mb={4}>
      <Typography variant="h5" align="center">
        Overview
      </Typography>
      <IconButton aria-label="refresh">
        <RefreshIcon />
      </IconButton>
    </Grid>

    <StatisticsWidgetsContainer />
  </Grid>
);

const StatisticsWidgetsContainer = () => (
  <Grid container spacing={3}>
    <Widget value="10,000" icon={<UserIcon />} color="#4f8ebd" title="Total Users" />
    <Widget value="500" icon={<MonitorIcon />} color="#62c462" title="Active Sessions" />
    <Widget value="$30,000" icon={<DollarSignIcon />} color="#ed9121" title="Revenue" />
    <Widget value="7" icon={<NotificationImportantIcon />} color="#ef4444" title="Notifications" />
  </Grid>
);

const Widget = ({ value, icon: Icon, color, title }) => (
  <Paper
    elevation={3}
    sx={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: 2,
      gap: 1,
    }}
  >
    <Icon style={{ fontSize: 40, color }} />
    <Typography variant="h6" color="inherit">
      {title}
    </Typography>
    <Typography variant="body1" color="inherit">
      {value}
    </Typography>
  </Paper>
);

const theme = {
  palette: {
    primary: { main: '#4f8ebd' },
    secondary: { main: '#62c462' },
    accent: { main: '#ed9121' },
    warning: { main: '#ef4444' },
  },
};

export default AppWrapper;