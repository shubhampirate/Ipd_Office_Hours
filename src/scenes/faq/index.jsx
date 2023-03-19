import { Box, useTheme } from "@mui/material";
import Header from "../../components/Header";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { tokens } from "../../theme";
import baseUrl from "../../baseUrl";
import { useState, useEffect } from "react";
import { format } from 'date-fns';

const FAQ = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

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
  var i = 0;
  return (
    <Box m="20px">
      <Header title="Notifications" subtitle="List of Notifications" />
      {
        notification.map((item) => {
          i++;
          return (
          <Accordion defaultExpanded key={i}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography color={colors.greenAccent[500]} variant="h5">
                {item.title}
              </Typography>
              <Box marginLeft="auto">
                <Typography variant="body2">
                  {item.sender}
                </Typography>
              </Box>
              <Box marginLeft="auto">
              <Typography variant="body2">
                {format(new Date(item.sent_at), 'dd/MM/yyyy HH:mm')}
              </Typography>
            </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Typography>
                {item.description}
              </Typography>
            </AccordionDetails>
          </Accordion>);
       })
      }
    </Box>
  );
};

export default FAQ;
