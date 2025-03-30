package edu.usc.ir.geo.gazetteer.api;

import edu.usc.ir.geo.gazetteer.GeoNameResolver;
import edu.usc.ir.geo.gazetteer.domain.Location;
import edu.usc.ir.geo.gazetteer.service.Launcher;

import javax.ws.rs.DefaultValue;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.List;
import java.util.logging.Logger;

@Path("/search")
@Produces(MediaType.APPLICATION_JSON)
public class SearchResource {

    public static final String SEARCH = "s";
    public static final String COUNT  = "c";
    private static final Logger LOG = Logger.getLogger(SearchResource.class.getName());

    private final GeoNameResolver resolver;

    public SearchResource() {
        String indexPath = System.getProperty(Launcher.INDEX_PATH_PROP);
        if (indexPath == null || indexPath.isEmpty()) {
            throw new IllegalStateException("Set Index Path with system property " + Launcher.INDEX_PATH_PROP);
        }
        try {
            LOG.info("Initialising searcher from index " + indexPath);
            this.resolver = new GeoNameResolver(indexPath);
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    @GET
    public Response getSearchResults(
            @QueryParam(SEARCH) List<String> search,
            @DefaultValue("1") @QueryParam(COUNT) int count) throws IOException {

        if (search == null || search.isEmpty() || count < 1) {
            return Response.status(Response.Status.BAD_REQUEST).build();
        }

        HashMap<String, List<Location>> result = resolver.searchGeoName(search, count);
        try (ByteArrayOutputStream arrayOutputStream = new ByteArrayOutputStream();
             PrintStream stream = new PrintStream(arrayOutputStream, true, StandardCharsets.UTF_8.name())) {
            GeoNameResolver.writeResultJson(result, stream);
            return Response.status(Response.Status.OK)
                    .entity(arrayOutputStream.toString(StandardCharsets.UTF_8.name()))
                    .build();
        }
    }
}
