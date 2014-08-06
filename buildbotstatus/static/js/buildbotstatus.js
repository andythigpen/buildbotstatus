(function() {

    var web_api_extention = 'buildbotstatus.extension.Buildbotstatus';
    var refresh_url = '/api/extensions/'+web_api_extention+'/refresh/';
    var field_id = 'buildbotstatus_status';

    var page = RB.PageManager.getPage();
    var el = $('#field_'+field_id);
    if (!page || !el.length) {
        return;
    }
    var view = page.reviewRequestEditorView;
    var model = view.model;

    RB.BuildbotstatusView = Backbone.View.extend({
        template: _.template([
            '<% if (!statuses) { %>',
            '  <img src="<%= spinner_url %>"',
            '    class="loading-indicator" width="16" height="16" ',
            '    border="0" alt="" />',
            '<% } else { %>',
            '  <table class="buildbot-table">',
            '  <% _.each(statuses, function(status) { %>',
            '    <tr>',
            '      <td><%= status.builderName %></td>',
            '      <td class="<%= status.cssClass %>"><a href="<%= status.url %>"><%= status.result %></a></td>',
            '    </tr>',
            '  <% }); %>',
            '  <% if (statuses.length == 0) { %>',
            '    <tr><td>None found - click <em>Refresh Buildbot Status</em> above to display.</td></tr>',
            '  <% } %>',
            '  </table>',
            '<% } %>'
        ].join('')),

        initialize: function() {
            this.render();
        },
        render: function() {
            this.$el.html(this.template(this.options));
            view._scheduleResizeLayout();
        }
    });

    var options = {
        spinner_url: STATIC_URLS['rb/images/spinner.gif'],
        el: el
    };
    if (typeof(buildbotstatus_initial) != 'undefined') {
        options['statuses'] = buildbotstatus_initial;
        buildbotstatus_initial = null;
    }
    var statusView = new RB.BuildbotstatusView(options);

    var fieldInfo = {
        fieldID: field_id,
        useExtraData: true,
        formatter: function(view, data, $el) {
            statusView.options.statuses = JSON.parse(data);
            statusView.render();
        }
    };

    function refresh_status(data) {
        page.reviewRequestEditorView.model.setDraftField(
            field_id,
            data.buildbotstatus_refresh,
            _.defaults({
                error: function(error) {
                    view._formatField(fieldInfo);
                    view._$warning
                        .delay(6000)
                        .fadeOut(400, function() {
                            $(this).hide();
                        })
                        .show()
                        .html(error.errorText);
                },
                success: function() {
                    view._formatField(fieldInfo);
                    view.showBanner();
                },
            }, fieldInfo),
            this);
    }

    $(document).on('click', '#buildbot-status', function() {
        statusView.options.statuses = null;
        statusView.render();

        var params = {
            'review_request_id': model.get('reviewRequest').id
        };

        $.ajax(refresh_url, {
            'data'      : params,
            'dataType'  : 'json',
            'success'   : refresh_status,
            'type'      : 'POST'
        });
    });
})();
