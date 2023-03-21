import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockDataTeam } from "../../data/mockData";
import AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import LockOpenOutlinedIcon from "@mui/icons-material/LockOpenOutlined";
import SecurityOutlinedIcon from "@mui/icons-material/SecurityOutlined";
import Header from "../../components/Header";
import { useState, useEffect } from "react";
import baseUrl from "../../baseUrl";

const Team = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [user, setUser] = useState([]);

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

		fetch(baseUrl + "all_employees/", requestOptions)
			.then((response) => response.json())
			.then((result) => {
        console.log(result);
        result.map((item, index) => {
          item.id = index+1
          item.efficiency = item.efficiency.map((item) => item.efficiency)
          if(item.user === localStorage.getItem('email')){ 
            item.name = "You";
          }
          return(item)
        });
				setUser(result);
			})
			.catch((error) => console.log("error", error));
  }, []);

  const columns = [
    { field: "id", headerName: "ID" },
    {
      field: "name",
      headerName: "Name",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "efficiency",
      headerName: "Efficiency",
      type: "number",
      headerAlign: "left",
      align: "left",
      renderCell: ({ row: { efficiency } }) => {
        console.log(efficiency);
        efficiency.length === 0 ? (efficiency = [0]) : (efficiency = efficiency);
        let eff_val = efficiency[efficiency.length-1]
        return (
            <Typography color={colors.grey[100]} sx={{ ml: "5px" }}>
              {eff_val}
            </Typography>
        );
      },
    },
    {
      field: "user",
      headerName: "Email",
      flex: 1,
    },
    {
      field: "role",
      headerName: "Role",
      flex: 1,
      renderCell: ({ row: { role } }) => {
        return (
          <Box
            width="60%"
            m="0 auto"
            p="5px"
            display="flex"
            justifyContent="center"
            backgroundColor={
              role === "Admin"
                ? colors.greenAccent[600]
                : role === "Team Leader"
                ? colors.greenAccent[700]
                : colors.greenAccent[700]
            }
            borderRadius="4px"
          >
            {role === "Admin" && <AdminPanelSettingsOutlinedIcon />}
            {role === "Team Leader" && <SecurityOutlinedIcon />}
            {role === "Employee" && <LockOpenOutlinedIcon />}
            <Typography color={colors.grey[100]} sx={{ ml: "5px" }}>
              {role}
            </Typography>
          </Box>
        );
      },
    },
  ];
  return (
    <Box m="20px">
      <Header title="TEAM" subtitle="Managing the Team Members" />
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
        }}
      >
        <DataGrid checkboxSelection rows={user} columns={columns} />
      </Box>
    </Box>
  );
};

export default Team;
