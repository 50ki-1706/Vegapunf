import useDashBoard from './hooks/useDashBoard';

const DashboardPage = () => {
  const message = useDashBoard();

  return <div>{message || 'Loading...'}</div>;
};

export default DashboardPage;
