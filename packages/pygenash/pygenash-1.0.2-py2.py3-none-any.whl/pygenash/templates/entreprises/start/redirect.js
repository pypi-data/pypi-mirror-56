
// user choice from display
var choice = _INPUT_.choice.selected;

// Create the targeted record
var refTarget = nash.instance.from("${nash.ws.private.url}")
    .createRecord('ref:entreprises/' + choice)
    .setAuthor(nash.record.description().author)
    .save();

log.info('formUid = {} | choice = {} | target record = {}', nash.record.description().formUid, choice, refTarget);

// redirect
return {
    url: _CONFIG_.get('nash.web.public.url')
        .concat('/record/')
        .concat(refTarget)
};