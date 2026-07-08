javascript
import React from 'react';
import { Box, Text, Flex } from '@chakra-ui/react';

const DarkThemeProvider = ({ children }) => {
  return (
    <Box bg="gray.900" color="white">
      {children}
    </Box>
  );
};

const StatisticsWidgetContainer = () => (
  <Flex direction="column" gap={4} p={8}>
    <Text fontWeight="bold">Total Users</Text>
    <Text>12,345</Text>
    <Text fontWeight="bold">Active Projects</Text>
    <Text>987</Text>
    <Text fontWeight="bold">Monthly Revenue</Text>
    <Text>$678,901.23</Text>
    <Text fontWeight="bold">Failed Tasks</Text>
    <Text>456</Text>
  </Flex>
);

const DashboardOverviewPage = () => (
  <DarkThemeProvider>
    <Box p={8} borderBottomWidth="1px" borderBottomColor="gray.700">
      <Text fontSize="2xl" fontWeight="bold">Dashboard Overview</Text>
    </Box>
    <StatisticsWidgetContainer />
  </DarkThemeProvider>
);

const App = () => (
  <DashboardOverviewPage />
);
export default App;