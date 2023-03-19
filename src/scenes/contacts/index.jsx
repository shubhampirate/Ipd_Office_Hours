import { Box } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
//import { mockDataNotifications } from "../../data/mockData";
import Header from "../../components/Header";
import { useTheme } from "@mui/material";
import baseUrl from "../../baseUrl";
import { useState, useEffect } from "react";

const Contacts = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const columns = [
    { field: "id", headerName: "ID", flex: 0.15 },
    //{ field: "registrarId", headerName: "Registrar ID" },
    {
      field: "sender",
      headerName: "Email",
      flex: 0.33,
    },
    {
      field: "title",
      headerName: "Title",
      flex: 0.50,
      cellClassName: "name-column--cell",
    },
    {
      field: "description",
      headerName: "Notification",
      flex: 1,
    },
  ];

  const [notification, setNotification] = useState([]);

  useEffect(() => {
    var myHeaders = new Headers();
    myHeaders.append(
      "Authorization",
      "Token "+localStorage.getItem('token')
    );
    myHeaders.append(
      "Cookie",
      "csrftoken=fQ5GcS3afHVVVyREFENw1Ub54RZgwlMkIFicrHrxOrddyB7xgNi46AaN5B6A4090; sessionid=vkfter6wndyr2xly3808yhu1meqwl3gn"
    );

    var requestOptions = {
			method: "GET",
			headers: myHeaders,
			redirect: "follow",
		};

		fetch(baseUrl + "notification/", requestOptions)
			.then((response) => response.json())
			.then((result) => {
        console.log(result)
				setNotification(result);
			})
			.catch((error) => console.log("error", error));
  }, []);

  return (
    <Box m="20px">
      <Header
        title="Notifications"
        subtitle="List of Notifications"
      />
      <Box
        m="40px 0 0 0"
        height="75vh"
        sx={{
          "& .MuiDataGrid-root": {
            border: "none",
          },
          "& .MuiDataGrid-cell": {
            borderBottom: "none",
          },
          "& .name-column--cell": {
            color: colors.greenAccent[300],
          },
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: colors.blueAccent[700],
            borderBottom: "none",
          },
          "& .MuiDataGrid-virtualScroller": {
            backgroundColor: colors.primary[400],
          },
          "& .MuiDataGrid-footerContainer": {
            borderTop: "none",
            backgroundColor: colors.blueAccent[700],
          },
          "& .MuiCheckbox-root": {
            color: `${colors.greenAccent[200]} !important`,
          },
          "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
            color: `${colors.grey[100]} !important`,
          },
        }}
      >
        <DataGrid
          rows={notification} //{mockDataNotifications}
          columns={columns}
          components={{ Toolbar: GridToolbar }}
        />
      </Box>
    </Box>
  );
};

export default Contacts;
